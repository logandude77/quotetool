"""Orient imported meshes: largest face down, origin at axis intersection."""

from __future__ import annotations

import numpy as np
import pyvista as pv


def _dominant_face_normal(mesh: pv.PolyData) -> np.ndarray:
    surf = mesh.extract_surface(algorithm=None).triangulate()
    surf = surf.compute_cell_sizes(length=False, area=True, volume=False)
    surf = surf.compute_normals(cell_normals=True, point_normals=False)

    normals = np.asarray(surf.cell_data["Normals"])
    areas = np.asarray(surf.cell_data["Area"])

    buckets: dict[tuple[float, float, float], float] = {}
    for normal, area in zip(normals, areas):
        if area <= 0:
            continue
        unit = normal / np.linalg.norm(normal)
        key = tuple(np.round(unit, 1))
        if key[2] < 0:
            key = (-key[0], -key[1], -key[2])
        buckets[key] = buckets.get(key, 0.0) + float(area)

    if not buckets:
        return np.array([0.0, 0.0, 1.0])

    dominant = np.array(max(buckets, key=buckets.get), dtype=float)
    norm = np.linalg.norm(dominant)
    if norm < 1e-9:
        return np.array([0.0, 0.0, 1.0])
    return dominant / norm


def _rotation_to_align(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    source = source / np.linalg.norm(source)
    target = target / np.linalg.norm(target)
    cross = np.cross(source, target)
    dot = float(np.clip(np.dot(source, target), -1.0, 1.0))

    if np.linalg.norm(cross) < 1e-8:
        if dot > 0:
            return np.eye(3)
        # 180° flip around X when vectors oppose
        return np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=float)

    skew = np.array(
        [
            [0, -cross[2], cross[1]],
            [cross[2], 0, -cross[0]],
            [-cross[1], cross[0], 0],
        ],
        dtype=float,
    )
    return np.eye(3) + skew + skew @ skew * (1 / (1 + dot))


def orient_largest_face_down(mesh: pv.PolyData) -> pv.PolyData:
    """Rotate so the largest flat face rests on the XY plane (normal along -Z)."""
    oriented = mesh.copy(deep=True)
    normal = _dominant_face_normal(oriented)
    rotation = _rotation_to_align(normal, np.array([0.0, 0.0, -1.0]))
    oriented.points = oriented.points @ rotation.T

    xmin, xmax, ymin, ymax, zmin, _ = oriented.bounds
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    oriented.translate((-cx, -cy, -zmin), inplace=True)
    return oriented
