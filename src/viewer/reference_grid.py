"""World-fixed reference grid centered at the origin (0, 0, 0)."""

from __future__ import annotations

import math

import numpy as np
import pyvista as pv

_MAX_LINES_PER_AXIS = 120
_MIN_HALF_EXTENT = 250.0


def _nice_spacing(span: float) -> float:
    if span <= 0:
        return 1.0
    raw = span / 20
    magnitude = 10 ** math.floor(math.log10(raw))
    norm = raw / magnitude
    if norm < 1.5:
        nice = 1.0
    elif norm < 3.5:
        nice = 2.0
    elif norm < 7.5:
        nice = 5.0
    else:
        nice = 10.0
    return nice * magnitude


def _half_extent(mesh: pv.PolyData, spacing: float) -> float:
    xmin, xmax, ymin, ymax, _, zmax = mesh.bounds
    half_xy = max(max(abs(xmin), abs(xmax)), max(abs(ymin), abs(ymax)), spacing * 4)
    half_z = max(zmax, spacing * 4)
    half = max(half_xy, half_z, _MIN_HALF_EXTENT)

    while (2 * half / spacing) > _MAX_LINES_PER_AXIS:
        spacing *= 2
    return half, spacing


def build_reference_grid(mesh: pv.PolyData) -> tuple[pv.PolyData, float]:
    """XY lines through origin on Z=0; single Z axis with unit notches."""
    xmin, xmax, ymin, ymax, _, zmax = mesh.bounds
    span = max(xmax - xmin, ymax - ymin, zmax, 1e-6)
    spacing = _nice_spacing(span)
    half, spacing = _half_extent(mesh, spacing)

    segments: list[pv.PolyData] = []
    coord = -half
    while coord <= half + spacing * 0.01:
        segments.append(pv.Line((-half, coord, 0.0), (half, coord, 0.0)))
        segments.append(pv.Line((coord, -half, 0.0), (coord, half, 0.0)))
        coord += spacing

    z_top = max(mesh.bounds[5], spacing * 2)
    segments.append(pv.Line((0.0, 0.0, 0.0), (0.0, 0.0, z_top)))

    tick = spacing * 0.1
    z = 0.0
    while z <= z_top + spacing * 0.01:
        segments.append(pv.Line((0.0, 0.0, z), (tick, 0.0, z)))
        segments.append(pv.Line((0.0, 0.0, z), (0.0, tick, z)))
        z += spacing

    merged = segments[0] if len(segments) == 1 else pv.merge(segments)
    return merged, spacing
