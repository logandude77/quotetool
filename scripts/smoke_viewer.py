"""Smoke check: OCC viewer displays a synthetic STEP shape."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PyQt5.QtWidgets import QApplication

from src.analyzer.step_loader import load_step
from src.viewer.viewport import OccViewport

app = QApplication(sys.argv)
vp = OccViewport()
shape = load_step("tests/fixtures/block_10x20x30.step")
vp.show_shape(shape)
print("viewer smoke OK")
app.quit()
