"""PySide6 STEP viewer entry (used after OSQ launcher)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def run_viewer(step_path: Path | None = None) -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    if step_path is not None:
        window.load_path(step_path)
    window.show()
    return app.exec()


def main() -> int:
    parser = argparse.ArgumentParser(description="Open Shop Quote 3D viewer")
    parser.add_argument(
        "step_file",
        nargs="?",
        help="Path to a .step or .stp file to load immediately",
    )
    args = parser.parse_args()
    path = Path(args.step_file).expanduser() if args.step_file else None
    return run_viewer(path)


if __name__ == "__main__":
    raise SystemExit(main())
