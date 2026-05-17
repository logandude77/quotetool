"""Load STEP files into a display mesh without UI dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tempfile

import cadquery as cq
import pyvista as pv


@dataclass(frozen=True)
class StepLoadResult:
    ok: bool
    path: Path
    mesh: pv.PolyData | None = None
    solid_count: int = 0
    error: str | None = None


def load_step(path: str | Path) -> StepLoadResult:
    step_path = Path(path).expanduser().resolve()

    if not step_path.exists():
        return StepLoadResult(ok=False, path=step_path, error="File does not exist.")

    if step_path.suffix.lower() not in {".step", ".stp"}:
        return StepLoadResult(
            ok=False,
            path=step_path,
            error="Expected a .step or .stp file.",
        )

    try:
        shape = cq.importers.importStep(str(step_path))
        solid_count = len(shape.solids().vals()) if hasattr(shape, "solids") else 1

        with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp:
            stl_path = Path(tmp.name)

        try:
            cq.exporters.export(shape, str(stl_path))
            mesh = pv.read(stl_path)
        finally:
            if stl_path.exists():
                stl_path.unlink()

        if mesh.n_points == 0:
            return StepLoadResult(
                ok=False,
                path=step_path,
                error="STEP imported but produced an empty mesh.",
            )

        return StepLoadResult(
            ok=True,
            path=step_path,
            mesh=mesh,
            solid_count=solid_count,
        )
    except Exception as exc:  # noqa: BLE001 - surface load failures to UI
        return StepLoadResult(ok=False, path=step_path, error=str(exc))
