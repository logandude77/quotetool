"""Run pytest in the quotetool conda env."""
import subprocess
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
subprocess.check_call(
    [sys.executable, "-m", "pytest", "tests/", "-q"],
    cwd=repo,
)
