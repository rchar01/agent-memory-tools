# Day-2 Operations

This guide covers updating the installed CLI, using editable installs during development, backing up memory data, and verifying the store after changes.

## Update an Installed CLI

If the package was installed from this local repository with `pipx`, update from the repository directory:

```bash
git pull
make update
```

`make update` runs backup, tests, reinstall, and memory verification.

The direct `pipx` equivalent is:

```bash
pipx install --force .
agent-memory --help
agent-memory verify
```

If reinstall cannot resolve the local package, use the explicit local workflow:

```bash
pipx uninstall agent-memory-tools
make install
agent-memory verify
```

## Active Development Install

When changing the tool frequently, use an editable install:

```bash
pipx uninstall agent-memory-tools
make install-editable
```

With an editable install, changes in this checkout are reflected by the installed `agent-memory` command. Keep the checkout in place. If you move or delete it, reinstall normally.

After code changes:

```bash
python3 -m pytest -o addopts='' tests
agent-memory --help
agent-memory verify
```

Or use:

```bash
make test
make verify
```

## Back Up Memory Data

The CLI package and the memory data are separate. Reinstalling the CLI should not delete memory files, but backup before major cleanup, schema changes, or tool upgrades.

Create a default backup:

```bash
make backup
```

The default output is a timestamped archive in a sibling `backups/` directory next to the active memory directory.

Create a backup at a specific path:

```bash
agent-memory backup --output ~/backups/agent-memory-before-upgrade.tar.gz
```

Create a backup inside a chosen directory:

```bash
agent-memory backup --output ~/backups/
```

The archive contains the memory directory under a top-level `memory/` folder.

## Safe Upgrade Checklist

Before updating:

```bash
make verify
make backup
```

Update the CLI:

```bash
make reinstall
```

After updating:

```bash
agent-memory --help
agent-memory verify
agent-memory retrieve --query "smoke test" --limit 1
```

The one-command local workflow is:

```bash
make update
```

## Recovery From a Bad Tool Release

If a new version behaves incorrectly:

```bash
pipx uninstall agent-memory-tools
git checkout <known-good-ref>
pipx install .
agent-memory verify
```

If memory files were damaged by an operation, restore manually from the latest backup archive after inspecting it. This package intentionally provides backup creation only; restore is not automated because overwriting memory data is destructive and should be a deliberate human action.

## Versioning Policy

Before sharing a new release or reinstalling across agent hosts:

```bash
python3 -m pytest -o addopts='' tests
agent-memory backup
```

Then bump `version` in `pyproject.toml` when the CLI behavior changes. Keep memory data format changes documented in this file and in the relevant specification docs.
