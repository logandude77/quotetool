"""Application window — file picking and status only."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core import load_step
from src.viewer import StepViewport


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("quotetool — STEP viewer")
        self.resize(1100, 760)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        toolbar = QHBoxLayout()
        open_btn = QPushButton("Open STEP…")
        open_btn.clicked.connect(self.open_step_file)
        toolbar.addWidget(open_btn)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.viewport = StepViewport()
        layout.addWidget(self.viewport, stretch=1)

        self.status = QLabel("Open a .step or .stp file to begin.")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)

    def open_step_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open STEP file",
            "",
            "STEP files (*.step *.stp);;All files (*.*)",
        )
        if not path:
            return
        self.load_path(Path(path))

    def load_path(self, path: Path) -> None:
        result = load_step(path)
        if not result.ok or result.mesh is None:
            self.viewport.clear()
            self.status.setText(f"Failed to load {path.name}: {result.error}")
            QMessageBox.warning(self, "Load failed", result.error or "Unknown error.")
            return

        self.viewport.show_mesh(result.mesh)
        spacing = self.viewport.grid_spacing()
        spacing_text = f", grid unit ≈ {spacing:g}" if spacing else ""
        self.status.setText(
            f"Loaded {result.path.name} — {result.solid_count} solid(s), "
            f"{result.mesh.n_points:,} vertices{spacing_text}. "
            f"Origin at axis center; largest face down."
        )
