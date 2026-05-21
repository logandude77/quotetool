"""OCC AIS/V3d viewport — display only (Mayo graphics/gui pattern)."""

from __future__ import annotations

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Display.backend import load_backend

# PyQt5 matches pythonocc display on Windows (conda PySide6 can DLL-conflict with OCC).
load_backend("pyqt5")

from OCC.Display.qtDisplay import qtViewer3d  # noqa: E402


class OccViewport(qtViewer3d):
    """Embeds AIS_InteractiveContext + V3d_View; no file I/O or analysis."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.InitDriver()
        self._current_ais = None

    def show_shape(self, shape: TopoDS_Shape) -> None:
        """Display a B-rep with shaded faces and visible edges."""
        self._display.EraseAll()
        # OCCViewer default drawer enables face boundary edges (Mayo-style readability).
        self._display.DisplayShape(shape, update=True, color="SILVER")
        self._display.FitAll()
        self._display.Repaint()

    def clear(self) -> None:
        self._display.EraseAll()
        self._current_ais = None
        self._display.Repaint()
