"""3D viewport wrapper — display only, no file I/O."""

from __future__ import annotations

import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QVBoxLayout, QWidget

from src.viewer.reference_grid import build_reference_grid

_BG_TOP = "#3a3f47"
_BG_BOTTOM = "#c4c9d2"
_GRID_COLOR = "#b8c6d8"
_PART_COLOR = "#b0b5be"


class StepViewport(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter = QtInteractor(self)
        layout.addWidget(self.plotter.interactor)
        self._grid_spacing: float | None = None
        self._reset_scene()

    def _apply_background(self) -> None:
        self.plotter.set_background(_BG_BOTTOM, top=_BG_TOP)

    def _apply_reference_grid(self, mesh: pv.PolyData) -> None:
        grid, spacing = build_reference_grid(mesh)
        self._grid_spacing = spacing
        self.plotter.add_mesh(
            grid,
            color=_GRID_COLOR,
            line_width=1,
            opacity=0.38,
            lighting=False,
            pickable=False,
        )

    def _add_part(self, mesh: pv.PolyData) -> None:
        self.plotter.add_mesh(
            mesh,
            color=_PART_COLOR,
            pbr=True,
            metallic=0.85,
            roughness=0.3,
            smooth_shading=True,
            show_edges=False,
        )

    def _reset_scene(self, mesh: pv.PolyData | None = None) -> None:
        self.plotter.clear()
        self._apply_background()
        self.plotter.show_axes()
        if mesh is not None:
            self._add_part(mesh)
            self._apply_reference_grid(mesh)

    def show_mesh(self, mesh: pv.PolyData) -> None:
        self._reset_scene(mesh)
        self.plotter.reset_camera()

    def grid_spacing(self) -> float | None:
        return self._grid_spacing

    def clear(self) -> None:
        self._grid_spacing = None
        self._reset_scene()

    def closeEvent(self, event) -> None:  # noqa: N802
        self.plotter.close()
        super().closeEvent(event)
