"""3D viewport wrapper — display only, no file I/O."""

from __future__ import annotations

import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QVBoxLayout, QWidget

from src.core.step_units import LengthUnit

_BG_TOP = "#3a3f47"
_BG_BOTTOM = "#c4c9d2"
_GRID_COLOR = "#6eb5f0"
_PART_COLOR = "#c8ccd4"
_EDGE_COLOR = "#5c636e"


class StepViewport(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter = QtInteractor(self)
        layout.addWidget(self.plotter.interactor)
        self._length_unit: LengthUnit | None = None
        self._reset_scene()

    def _apply_background(self) -> None:
        self.plotter.set_background(_BG_BOTTOM, top=_BG_TOP)

    def _apply_grid(self, mesh: pv.PolyData | None = None) -> None:
        """Single PyVista grid (same approach as first main publish)."""
        kwargs: dict = {
            "color": _GRID_COLOR,
            "location": "back",
            "font_size": 10,
        }
        if mesh is not None:
            kwargs["bounds"] = mesh.bounds
        self.plotter.show_grid(**kwargs)

    def _extract_part_edges(self, mesh: pv.PolyData) -> pv.PolyData | None:
        creases = mesh.extract_feature_edges(
            boundary_edges=False,
            feature_edges=True,
            manifold_edges=False,
            non_manifold_edges=False,
            feature_angle=30,
        )
        outline = mesh.extract_feature_edges(
            boundary_edges=True,
            feature_edges=False,
            manifold_edges=False,
            non_manifold_edges=False,
        )
        parts = [m for m in (creases, outline) if m.n_points > 0]
        if not parts:
            return None
        if len(parts) == 1:
            return parts[0]
        return pv.merge(parts)

    def _add_part(self, mesh: pv.PolyData) -> None:
        self.plotter.add_mesh(
            mesh,
            color=_PART_COLOR,
            pbr=True,
            metallic=0.82,
            roughness=0.32,
            smooth_shading=True,
            show_edges=False,
            reset_camera=False,
        )
        edges = self._extract_part_edges(mesh)
        if edges is not None:
            self.plotter.add_mesh(
                edges,
                color=_EDGE_COLOR,
                line_width=1.5,
                lighting=False,
                pickable=False,
                reset_camera=False,
            )

    def _reset_scene(
        self,
        mesh: pv.PolyData | None = None,
        length_unit: LengthUnit | None = None,
    ) -> None:
        self.plotter.clear()
        self._apply_background()
        if length_unit is not None:
            self._length_unit = length_unit
        if mesh is not None:
            self._add_part(mesh)
            self.plotter.reset_camera(bounds=mesh.bounds)
            self.plotter.camera.clipping_range = (0.1, 1_000_000.0)
            self._apply_grid(mesh)

    def show_mesh(self, mesh: pv.PolyData, length_unit: LengthUnit) -> None:
        self._reset_scene(mesh, length_unit)

    def length_unit(self) -> LengthUnit | None:
        return self._length_unit

    def clear(self) -> None:
        self._length_unit = None
        self._reset_scene()

    def closeEvent(self, event) -> None:  # noqa: N802
        self.plotter.close()
        super().closeEvent(event)
