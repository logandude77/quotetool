"""3D viewport wrapper — display only, no file I/O."""

from __future__ import annotations

import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QVBoxLayout, QWidget

# Vertical gradient: darker grey (top) → lighter grey (bottom)
_BG_TOP = "#4a4f57"
_BG_BOTTOM = "#c8ccd4"
_GRID_COLOR = "#3b82f6"
_PART_COLOR = "#4a90d9"


class StepViewport(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter = QtInteractor(self)
        layout.addWidget(self.plotter.interactor)
        self._reset_scene()

    def _apply_background(self) -> None:
        # color = bottom; top = darker grey fading upward
        self.plotter.set_background(_BG_BOTTOM, top=_BG_TOP)

    def _apply_grid(self, mesh: pv.PolyData | None = None) -> None:
        kwargs: dict = {
            "color": _GRID_COLOR,
            "location": "back",
            "font_size": 10,
        }
        if mesh is not None:
            kwargs["bounds"] = mesh.bounds
        self.plotter.show_grid(**kwargs)

    def _reset_scene(self, mesh: pv.PolyData | None = None) -> None:
        self.plotter.clear()
        self._apply_background()
        self.plotter.add_axes()
        if mesh is not None:
            self.plotter.add_mesh(mesh, color=_PART_COLOR, show_edges=True)
        self._apply_grid(mesh)

    def show_mesh(self, mesh: pv.PolyData) -> None:
        self._reset_scene(mesh)
        self.plotter.reset_camera()

    def clear(self) -> None:
        self._reset_scene()

    def closeEvent(self, event) -> None:  # noqa: N802
        self.plotter.close()
        super().closeEvent(event)
