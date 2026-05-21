"""Tests for STEP loading and shape summary (synthetic fixtures only)."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.analyzer.step_loader import StepLoadError, load_step, summarize

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="module", autouse=True)
def ensure_fixtures() -> None:
    if not (FIXTURES / "block_10x20x30.step").exists():
        import subprocess
        import sys

        script = Path(__file__).resolve().parents[1] / "scripts" / "make_fixtures.py"
        subprocess.run([sys.executable, str(script)], check=True)


def test_load_block_bbox_and_volume() -> None:
    shape = load_step(FIXTURES / "block_10x20x30.step")
    stats = summarize(shape)
    assert stats.volume == pytest.approx(6000.0, rel=0.02)
    assert stats.dx == pytest.approx(10.0, rel=0.02)
    assert stats.dy == pytest.approx(20.0, rel=0.02)
    assert stats.dz == pytest.approx(30.0, rel=0.02)
    assert stats.face_count == 6


def test_load_block_with_hole() -> None:
    shape = load_step(FIXTURES / "block_with_hole.step")
    stats = summarize(shape)
    assert stats.volume > 0
    assert stats.face_count > 6


def test_load_block_with_pocket() -> None:
    shape = load_step(FIXTURES / "block_with_pocket.step")
    stats = summarize(shape)
    assert stats.volume > 0
    assert stats.face_count > 6


def test_missing_file_raises() -> None:
    with pytest.raises(StepLoadError, match="does not exist"):
        load_step(FIXTURES / "no_such_part.step")


def test_bad_extension_raises() -> None:
    with pytest.raises(StepLoadError, match="Expected"):
        load_step(__file__)


def test_corrupt_step_raises(tmp_path: Path) -> None:
    bad = tmp_path / "not_really.step"
    bad.write_text("this is not a STEP file", encoding="utf-8")
    with pytest.raises(StepLoadError):
        load_step(bad)
