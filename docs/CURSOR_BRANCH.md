# cursor/step-viewer

Cursor-generated Phase 1: open and view STEP files.

## Setup

```powershell
cd C:\Projects\quotetool
conda activate quotetool
pip install -r requirements.txt
```

## Run

```powershell
python -m src.main
```

Use **Open STEP…** and pick a `.step` or `.stp` file.

## Layout

- `src/core/step_loader.py` — STEP import (CadQuery) → PyVista mesh
- `src/viewer/viewport.py` — 3D widget only
- `src/ui/main_window.py` — file dialog and status
- `src/main.py` — thin entry point
