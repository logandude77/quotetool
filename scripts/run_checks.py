"""Generate fixtures, run pytest, smoke-test load_step."""
import subprocess
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.check_call([sys.executable, str(repo / "scripts" / "make_fixtures.py")], cwd=repo)
    subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-q"], cwd=repo)
    subprocess.check_call([sys.executable, str(repo / "scripts" / "smoke_loader.py")], cwd=repo)
    print("All checks passed.")


if __name__ == "__main__":
    main()
