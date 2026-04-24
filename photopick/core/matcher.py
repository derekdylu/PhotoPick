"""Pure matching logic shared by the CLI and the GUI."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable

JPG_EXTENSIONS: frozenset[str] = frozenset({".jpg", ".jpeg"})
RAW_EXTENSIONS: frozenset[str] = frozenset(
    {".cr2", ".cr3", ".nef", ".arw", ".dng", ".orf", ".rw2", ".pef", ".srw", ".x3f"}
)


class ComparisonMethod(str, Enum):
    ANCHOR_JPG = "anchor_jpg"
    ANCHOR_RAW = "anchor_raw"
    BOTH = "both"


def is_jpg(path: Path) -> bool:
    return path.suffix.lower() in JPG_EXTENSIONS


def is_raw(path: Path) -> bool:
    return path.suffix.lower() in RAW_EXTENSIONS


@dataclass(frozen=True)
class OrphanEntry:
    """A file that has no counterpart on the other side."""

    path: Path
    side: str  # "jpg" or "raw"

    @property
    def missing_side(self) -> str:
        return "raw" if self.side == "jpg" else "jpg"


@dataclass
class MatchResult:
    jpg_files: list[Path] = field(default_factory=list)
    raw_files: list[Path] = field(default_factory=list)
    orphans: list[OrphanEntry] = field(default_factory=list)

    @property
    def jpg_count(self) -> int:
        return len(self.jpg_files)

    @property
    def raw_count(self) -> int:
        return len(self.raw_files)


def _stem_index(files: Iterable[Path]) -> dict[str, list[Path]]:
    """Map basename → list of files with that basename (case-insensitive)."""
    index: dict[str, list[Path]] = {}
    for f in files:
        index.setdefault(f.stem.lower(), []).append(f)
    return index


def classify(
    jpg_files: list[Path],
    raw_files: list[Path],
    method: ComparisonMethod,
) -> MatchResult:
    """Identify orphan files according to the comparison method.

    - ANCHOR_JPG: list RAWs with no matching JPG (RAW orphans).
    - ANCHOR_RAW: list JPGs with no matching RAW (JPG orphans).
    - BOTH: both directions combined.
    """
    jpg_index = _stem_index(jpg_files)
    raw_index = _stem_index(raw_files)

    orphans: list[OrphanEntry] = []

    if method in (ComparisonMethod.ANCHOR_JPG, ComparisonMethod.BOTH):
        for raw in raw_files:
            if raw.stem.lower() not in jpg_index:
                orphans.append(OrphanEntry(path=raw, side="raw"))

    if method in (ComparisonMethod.ANCHOR_RAW, ComparisonMethod.BOTH):
        for jpg in jpg_files:
            if jpg.stem.lower() not in raw_index:
                orphans.append(OrphanEntry(path=jpg, side="jpg"))

    orphans.sort(key=lambda e: (e.side, str(e.path).lower()))

    return MatchResult(
        jpg_files=sorted(jpg_files, key=lambda p: str(p).lower()),
        raw_files=sorted(raw_files, key=lambda p: str(p).lower()),
        orphans=orphans,
    )


def find_raw_for_jpg(jpg_path: Path, raw_index: dict[str, list[Path]]) -> Path | None:
    """Look up the matching RAW for a given JPG path. Returns None if not found."""
    matches = raw_index.get(jpg_path.stem.lower())
    if not matches:
        return None
    return matches[0]
