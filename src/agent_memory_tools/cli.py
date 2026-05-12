from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .backup import create_backup
from .cleaner import archive_memory, find_duplicates, supersede_memory
from .index import regenerate_index
from .markdown import parse_input_file
from .paths import ensure_memory_tree, index_path, readme_path, resolve_memory_dir
from .retrieval import render_brief, retrieve_memories
from .verifier import verify_memory
from .writer import write_memory


README_TEXT = """# Memory System

This directory stores shared markdown memory for agents.

## Rules

- Do not load all memory into context.
- Use `agent-memory retrieve` for selective recall.
- Coders may retrieve memory but must not write it.
- Memory summarizers create entries with `agent-memory write`.
- Memory cleaners archive, supersede, and deduplicate entries.
- Store only durable knowledge useful for future tasks.

## Files

- `INDEX.md` - short searchable index.
- `entries/` - active memory entries.
- `archive/` - old or superseded memories.
"""


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    memory_dir = resolve_memory_dir(args.memory_dir)
    try:
        return args.func(args, memory_dir)
    except Exception as exc:
        print(f"agent-memory: error: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-memory", description="Local markdown memory tools for agents")
    parser.add_argument("--memory-dir", help="Memory directory; defaults to AGENT_MEMORY_DIR or ~/.local/share/agent-memory-tools/memory")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create the memory directory structure")
    init.set_defaults(func=cmd_init)

    retrieve = sub.add_parser("retrieve", help="Retrieve a compact brief of relevant active memories")
    retrieve.add_argument("--query", default="", help="Search query or task text")
    retrieve.add_argument("--project", default="", help="Current project name")
    retrieve.add_argument("--tags", default="", help="Comma-separated tags")
    retrieve.add_argument("--limit", type=int, default=3, help="Number of memories to return, max 5")
    retrieve.set_defaults(func=cmd_retrieve)

    write = sub.add_parser("write", help="Create a memory entry from JSON, simple YAML, or markdown frontmatter")
    write.add_argument("--input", required=True, help="Input file describing the memory entry")
    write.set_defaults(func=cmd_write)

    index_update = sub.add_parser("index-update", help="Regenerate INDEX.md from active entries")
    index_update.set_defaults(func=cmd_index_update)

    verify = sub.add_parser("verify", help="Verify memory store integrity")
    verify.add_argument("--json", action="store_true", help="Print machine-readable result")
    verify.set_defaults(func=cmd_verify)

    clean = sub.add_parser("clean", help="Conservative cleanup operations")
    group = clean.add_mutually_exclusive_group(required=True)
    group.add_argument("--find-duplicates", action="store_true", help="Report duplicate or overlapping active memories")
    group.add_argument("--archive", metavar="ID", help="Archive an active memory id")
    group.add_argument("--supersede", metavar="OLD_ID", help="Mark OLD_ID as superseded")
    clean.add_argument("--by", metavar="NEW_ID", help="Replacement id for --supersede")
    clean.add_argument("--reason", default="", help="Reason for archive operation")
    clean.set_defaults(func=cmd_clean)

    backup = sub.add_parser("backup", help="Create a gzipped backup archive of the memory directory")
    backup.add_argument("--output", help="Output .tar.gz path or directory; defaults to sibling backups/ directory")
    backup.set_defaults(func=cmd_backup)
    return parser


def cmd_init(args: argparse.Namespace, memory_dir: Path) -> int:
    ensure_memory_tree(memory_dir)
    if not index_path(memory_dir).exists():
        index_path(memory_dir).write_text("# Memory Index\n\n## Active Memories\n", encoding="utf-8")
    if not readme_path(memory_dir).exists():
        readme_path(memory_dir).write_text(README_TEXT, encoding="utf-8")
    print(f"Initialized memory directory: {memory_dir}")
    return 0


def cmd_retrieve(args: argparse.Namespace, memory_dir: Path) -> int:
    results = retrieve_memories(memory_dir, query=args.query, project=args.project, tags=args.tags, limit=args.limit)
    print(render_brief(results), end="")
    return 0


def cmd_write(args: argparse.Namespace, memory_dir: Path) -> int:
    ensure_memory_tree(memory_dir)
    entry = parse_input_file(Path(args.input).expanduser())
    write_memory(memory_dir, entry)
    print(f"Created memory: {entry.id}")
    return 0


def cmd_index_update(args: argparse.Namespace, memory_dir: Path) -> int:
    ensure_memory_tree(memory_dir)
    regenerate_index(memory_dir)
    print(f"Updated index: {index_path(memory_dir)}")
    return 0


def cmd_verify(args: argparse.Namespace, memory_dir: Path) -> int:
    result = verify_memory(memory_dir)
    if args.json:
        print(json.dumps({"ok": result.ok, "errors": result.errors, "warnings": result.warnings}, indent=2))
    else:
        if result.ok:
            print("Memory verification passed.")
        for warning in result.warnings:
            print(f"WARNING: {warning}")
        for error in result.errors:
            print(f"ERROR: {error}")
    return 0 if result.ok else 1


def cmd_clean(args: argparse.Namespace, memory_dir: Path) -> int:
    ensure_memory_tree(memory_dir)
    if args.find_duplicates:
        findings = find_duplicates(memory_dir)
        if findings:
            for finding in findings:
                print(finding)
        else:
            print("No duplicate or overlapping active memories found.")
        return 0
    if args.archive:
        target = archive_memory(memory_dir, args.archive, reason=args.reason)
        print(f"Archived {args.archive} -> {target}")
        return 0
    if args.supersede:
        if not args.by:
            raise ValueError("--supersede requires --by NEW_ID")
        supersede_memory(memory_dir, args.supersede, args.by)
        print(f"Marked {args.supersede} as superseded by {args.by}")
        return 0
    raise ValueError("no cleanup operation selected")


def cmd_backup(args: argparse.Namespace, memory_dir: Path) -> int:
    target = create_backup(memory_dir, args.output)
    print(f"Created backup: {target}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
