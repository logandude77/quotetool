import sys
from pathlib import Path
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analyzer.step_loader import StepLoadError, load_step, summarize

p = Path("tests/fixtures/block_10x20x30.step")
summarize(load_step(p))

bad = Path(tempfile.gettempdir()) / "bad_quotetool.step"
bad.write_text("not step", encoding="utf-8")
try:
    load_step(bad)
except StepLoadError:
    print("bad file OK")
else:
    raise SystemExit("expected StepLoadError")

print("smoke OK")
