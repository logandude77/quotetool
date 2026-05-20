"""Detect length units declared in a STEP file."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LengthUnit:
    """File length unit from STEP metadata."""

    name: str  # mm, in, cm, m


def detect_step_length_unit(path: Path) -> LengthUnit:
    """Read STEP schema text for declared length units (default mm)."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:400_000].upper()
    except OSError:
        return LengthUnit("mm")

    if re.search(
        r"SI_UNIT\s*\(\s*\$?\s*,\s*\.INCH\s*\.|"
        r"SI_UNIT\s*\(\s*\.INCH\s*\.|"
        r"INCH\b|"
        r"US_INCH",
        text,
    ):
        return LengthUnit("in")
    if re.search(r"SI_UNIT\s*\(\s*\.MILLI\s*\.\s*,\s*\.METRE\s*\.|MILLI.+METRE", text):
        return LengthUnit("mm")
    if re.search(r"SI_UNIT\s*\(\s*\.CENTI\s*\.\s*,\s*\.METRE\s*\.|CENTI.+METRE", text):
        return LengthUnit("cm")
    if re.search(r"SI_UNIT\s*\(\s*\$?\s*,\s*\.METRE\s*\.|SI_UNIT\s*\(\s*\.METRE\s*\.", text):
        return LengthUnit("m")
    return LengthUnit("mm")
