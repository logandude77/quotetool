"""Generate synthetic STEP fixtures (OCC primitives only — no customer geometry)."""

from __future__ import annotations

from pathlib import Path

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.STEPControl import STEPControl_AsIs, STEPControl_Writer

_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = _ROOT / "tests" / "fixtures"


def _write_step(shape, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = STEPControl_Writer()
    writer.Transfer(shape, STEPControl_AsIs)
    if writer.Write(str(path)) != 1:
        raise RuntimeError(f"Failed to write STEP: {path}")


def block_10() -> None:
    box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()
    _write_step(box, FIXTURES / "block_10x20x30.step")


def block_with_hole() -> None:
    outer = BRepPrimAPI_MakeBox(40.0, 40.0, 20.0).Shape()
    hole = BRepPrimAPI_MakeBox(gp_Pnt(15.0, 15.0, -2.0), 10.0, 10.0, 25.0).Shape()
    cut = BRepAlgoAPI_Cut(outer, hole)
    cut.Build()
    if not cut.IsDone():
        raise RuntimeError("Boolean cut for hole fixture failed")
    _write_step(cut.Shape(), FIXTURES / "block_with_hole.step")


def block_with_pocket() -> None:
    outer = BRepPrimAPI_MakeBox(50.0, 50.0, 25.0).Shape()
    pocket = BRepPrimAPI_MakeBox(gp_Pnt(10.0, 10.0, 15.0), 30.0, 30.0, 12.0).Shape()
    cut = BRepAlgoAPI_Cut(outer, pocket)
    cut.Build()
    if not cut.IsDone():
        raise RuntimeError("Boolean cut for pocket fixture failed")
    _write_step(cut.Shape(), FIXTURES / "block_with_pocket.step")


def main() -> None:
    block_10()
    block_with_hole()
    block_with_pocket()
    print(f"Wrote fixtures to {FIXTURES}")


if __name__ == "__main__":
    main()
