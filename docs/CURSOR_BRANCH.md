# cursor/step-viewer

Cursor-generated Phase 1: open and view STEP files.

## Setup (recommended — pip only, avoids Qt DLL conflicts)

If `quotetool` env is broken, recreate it once:

```powershell
conda deactivate
conda env remove -n quotetool -y
conda create -n quotetool python=3.12 pip -c conda-forge -y
conda activate quotetool
cd C:\Projects\quotetool
pip install cadquery PySide6 pyvista pyvistaqt
```

Do **not** mix `conda install pyside6/vtk` with `pip install` for those same packages.

Quick check:

```powershell
python -c "import cadquery, pyvista; from PySide6.QtWidgets import QApplication; print('OK')"
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
