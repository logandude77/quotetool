# cursor/fresh-start

Clean restart of Phase 1 on top of the original growable scaffold (`1871957` /
`c0f304a` on `main`), **without** the experimental branches piled on later:

- No OSQ CustomTkinter launcher
- No soft-grid / mesh-orient experiments from `cursor/soft-grid-origin`
- No merged `main` history after PR #1 (this branch stays at the pre-merge baseline)

## Run locally

```powershell
cd C:\Projects\quotetool
git checkout cursor/fresh-start
.\run.ps1
```

Or:

```powershell
conda activate quotetool
cd C:\Projects\quotetool
python -m src.main
```

## Build here

Use `@interface-skill` (personal skill in `~/.cursor/skills/interface-skill/`) for
loader, viewer, and measuring work. Port from Mayo/FreeCAD per `THIRD_PARTY_NOTICES`.

## Push the branch

```powershell
git push -u origin cursor/fresh-start
```
