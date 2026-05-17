# Branch strategy

| Branch | Owner | Purpose |
|--------|--------|---------|
| `main` | merged winners | Stable project; shared docs and license |
| `cursor/step-viewer` | Cursor | STEP viewer implementation (growable layout) |
| `claude/step-viewer` | Claude | Parallel experiment; compare and merge best ideas |

Compare branches on GitHub or locally:

```powershell
git fetch origin
git diff main..cursor/step-viewer
git diff main..claude/step-viewer
```

Merge the preferred branch into `main` when ready.
