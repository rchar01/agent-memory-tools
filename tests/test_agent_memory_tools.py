from __future__ import annotations

import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent_memory_tools.cli import main
from agent_memory_tools.retrieval import retrieve_memories
from agent_memory_tools.verifier import verify_memory


def write_input(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "memory.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_init_write_verify_retrieve(tmp_path, capsys):
    memory_dir = tmp_path / "memory"
    assert main(["--memory-dir", str(memory_dir), "init"]) == 0

    input_path = write_input(
        tmp_path,
        """
id: auth-token-format
project: backend
tags: [auth, jwt, dashboard]
importance: 0.9
summary: JWT validation now happens in shared backend middleware, and dashboard depends on token payload shape.
decisions:
  - Do not parse JWT tokens directly inside route handlers.
  - Use src/middleware/auth.ts for token validation.
impact:
  - Dashboard may break if token payload fields change.
related_projects: [backend, dashboard, workers]
important_files:
  - src/middleware/auth.ts
  - src/auth/jwt.ts
retrieve_when:
  - login
  - JWT validation
  - dashboard authentication
""".strip(),
    )

    assert main(["--memory-dir", str(memory_dir), "write", "--input", str(input_path)]) == 0
    result = verify_memory(memory_dir)
    assert result.ok, result.errors

    retrieved = retrieve_memories(memory_dir, query="dashboard token", project="dashboard", tags="auth,jwt")
    assert [item.entry.id for item in retrieved] == ["auth-token-format"]

    assert main(["--memory-dir", str(memory_dir), "retrieve", "--query", "dashboard token", "--project", "dashboard"]) == 0
    output = capsys.readouterr().out
    assert "auth-token-format" in output
    assert "Do not parse JWT tokens" in output


def test_write_rejects_secret(tmp_path):
    memory_dir = tmp_path / "memory"
    assert main(["--memory-dir", str(memory_dir), "init"]) == 0
    input_path = write_input(
        tmp_path,
        """
id: bad-secret
project: backend
tags: [auth]
importance: 0.5
summary: API_KEY=abcdefghijklmnopqrstuvwxyz123456 should not be stored.
""".strip(),
    )
    assert main(["--memory-dir", str(memory_dir), "write", "--input", str(input_path)]) == 1


def test_supersede_removes_old_entry_from_index(tmp_path):
    memory_dir = tmp_path / "memory"
    assert main(["--memory-dir", str(memory_dir), "init"]) == 0
    old = write_input(
        tmp_path,
        """
id: old-auth-token
project: backend
tags: [auth]
importance: 0.4
summary: Old auth token behavior.
""".strip(),
    )
    assert main(["--memory-dir", str(memory_dir), "write", "--input", str(old)]) == 0
    new = write_input(
        tmp_path,
        """
id: new-auth-token
project: backend
tags: [auth]
importance: 0.8
summary: New auth token behavior.
""".strip(),
    )
    assert main(["--memory-dir", str(memory_dir), "write", "--input", str(new)]) == 0
    assert main(["--memory-dir", str(memory_dir), "clean", "--supersede", "old-auth-token", "--by", "new-auth-token"]) == 0

    index = (memory_dir / "INDEX.md").read_text(encoding="utf-8")
    assert "### new-auth-token" in index
    assert "### old-auth-token" not in index
    assert verify_memory(memory_dir).ok


def test_backup_creates_archive_with_memory_tree(tmp_path):
    memory_dir = tmp_path / "memory"
    backup_dir = tmp_path / "backups"
    assert main(["--memory-dir", str(memory_dir), "init"]) == 0
    assert main(["--memory-dir", str(memory_dir), "backup", "--output", str(backup_dir)]) == 0

    backups = list(backup_dir.glob("agent-memory-backup-*.tar.gz"))
    assert len(backups) == 1
    with tarfile.open(backups[0], "r:gz") as archive:
        names = set(archive.getnames())
    assert "memory/INDEX.md" in names
    assert "memory/README.md" in names
