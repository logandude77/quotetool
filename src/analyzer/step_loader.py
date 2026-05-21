"""Load STEP into OpenCASCADE shapes — ported from Mayo io_occ patterns."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import TopoDS_Shape


class StepLoadError(Exception):
    """STEP file missing, unreadable, or produced no shape."""


@dataclass(frozen=True)
class ShapeSummary:
    """Bounding box, topology count, and volume for a loaded shape."""

    xmin: float
    ymin: float
    zmin: float
    xmax: float
    ymax: float
    zmax: float
    face_count: int
    volume: float

    @property
    def dx(self) -> float:
        return self.xmax - self.xmin

    @property
    def dy(self) -> float:
        return self.ymax - self.ymin

    @property
    def dz(self) -> float:
        return self.zmax - self.zmin


def load_step(path: str | Path) -> TopoDS_Shape:
    """Read a STEP file into a single TopoDS_Shape.

    Mayo-style flow: STEPControl_Reader → TransferRoots → OneShape.
    Raises StepLoadError on missing paths, bad extensions, or OCC read failures.
    """
    step_path = Path(path).expanduser().resolve()

    if not step_path.exists():
        raise StepLoadError(f"File does not exist: {step_path}")

    if step_path.suffix.lower() not in {".step", ".stp"}:
        raise StepLoadError("Expected a .step or .stp file.")

    reader = STEPControl_Reader()
    status = reader.ReadFile(str(step_path))
    if status != IFSelect_RetDone:
        raise StepLoadError(f"STEP reader could not read file (status={status}).")

    reader.TransferRoots()
    shape = reader.OneShape()
    if shape.IsNull():
        raise StepLoadError("STEP transferred but produced an empty shape.")

    return shape


def _compute_summary(shape: TopoDS_Shape) -> ShapeSummary:
    if shape.IsNull():
        raise StepLoadError("Cannot summarize a null shape.")

    box = Bnd_Box()
    brepbndlib.Add(shape, box, True)
    if box.IsVoid():
        raise StepLoadError("Shape has no bounding box.")

    xmin, ymin, zmin, xmax, ymax, zmax = box.Get()

    face_count = 0
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face_count += 1
        explorer.Next()

    props = GProp_GProps()
    brepgprop.VolumeProperties(shape, props)
    volume = props.Mass()

    return ShapeSummary(
        xmin=xmin,
        ymin=ymin,
        zmin=zmin,
        xmax=xmax,
        ymax=ymax,
        zmax=zmax,
        face_count=face_count,
        volume=volume,
    )


def format_summary(summary: ShapeSummary) -> str:
    """Human-readable summary for logs and the status bar."""
    return (
        f"bbox=({summary.xmin:.2f}, {summary.ymin:.2f}, {summary.zmin:.2f}) "
        f"-> ({summary.xmax:.2f}, {summary.ymax:.2f}, {summary.zmax:.2f}) "
        f"size=({summary.dx:.2f}x{summary.dy:.2f}x{summary.dz:.2f}) "
        f"faces={summary.face_count} volume={summary.volume:.2f}"
    )


def summarize(shape: TopoDS_Shape) -> ShapeSummary:
    """Print bbox, face count, and volume; return values for tests/UI."""
    summary = _compute_summary(shape)
    print(format_summary(summary))
    return summary
