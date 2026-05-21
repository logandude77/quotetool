"""Main window — File→Open and OCC viewer (no analysis in the UI layer)."""

from __future__ import annotations

from pathlib import Path

from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from src.analyzer.step_loader import (
    StepLoadError,
    format_summary,
    load_step,
    summarize as summarize_and_print,
)
from src.viewer import OccViewport


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Open Shop Quote — 3D View")
        self.resize(1100, 760)

        open_action = QAction("&Open STEP…", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_step_file)
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(open_action)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.viewport = OccViewport(central)
        layout.addWidget(self.viewport)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("File → Open STEP to begin.")

    def open_step_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open STEP file",
            "",
            "STEP files (*.step *.stp);;All files (*.*)",
        )
        if path:
            self.load_path(Path(path))

    def load_path(self, path: Path) -> None:
        try:
            shape = load_step(path)
            stats = summarize_and_print(shape)
        except StepLoadError as exc:
            self.viewport.clear()
            self.status.showMessage(f"Failed to load {path.name}: {exc}")
            QMessageBox.warning(self, "Load failed", str(exc))
            return

        self.viewport.show_shape(shape)
        self.status.showMessage(f"{path.name} — {format_summary(stats)}")
