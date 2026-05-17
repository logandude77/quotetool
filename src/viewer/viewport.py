"""3D viewport wrapper — display only, no file I/O."""

from __future__ import annotations

import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QVBoxLayout, QWidget


class StepViewport(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.plotter = QtInteractor(self)
        layout.addWidget(self.plotter.interactor)
        self.plotter.set_background("white")
        self.plotter.add_axes()

    def show_mesh(self, mesh: pv.PolyData) -> None:
        self.plotter.clear()
        self.plotter.add_axes()
        self.plotter.add_mesh(mesh, color="#4a90d9", show_edges=True)
        self.plotter.reset_camera()

    def clear(self) -> None:
        self.plotter.clear()
        self.plotter.add_axes()

    def closeEvent(self, event) -> None:  # noqa: N802
        self.plotter.close()
        super().closeEvent(event)
