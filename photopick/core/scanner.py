"""Filesystem walkers that produce JPG / RAW file lists."""

from __future__ import annotations

from pathlib import Path

from .matcher import is_jpg, is_raw


def scan_one_folder(folder: Path) -> tuple[list[Path], list[Path]]:
    """Walk a single folder and return (jpgs, raws)."""
    jpgs: list[Path] = []
    raws: list[Path] = []
    for p in folder.rglob("*"):
        if not p.is_file():
            continue
        if is_jpg(p):
            jpgs.append(p)
        elif is_raw(p):
            raws.append(p)
    return jpgs, raws


def scan_two_folders(jpg_folder: Path, raw_folder: Path) -> tuple[list[Path], list[Path]]:
    """Walk two folders and return (jpgs from first, raws from second)."""
    jpgs = [p for p in jpg_folder.rglob("*") if p.is_file() and is_jpg(p)]
    raws = [p for p in raw_folder.rglob("*") if p.is_file() and is_raw(p)]
    return jpgs, raws
