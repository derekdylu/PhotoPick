#!/usr/bin/env python3
"""PhotoPick CLI — thin wrapper around photopick.core.

For the Mac app, run: python -m photopick.ui.app
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from photopick.core import (
    ComparisonMethod,
    classify,
    scan_one_folder,
    scan_two_folders,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find (and optionally delete) orphaned RAW/JPG files."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        help="Folder to scan (single-folder mode). Omit to use --jpg-dir/--raw-dir.",
    )
    parser.add_argument("--jpg-dir", help="JPG folder (two-folder mode)")
    parser.add_argument("--raw-dir", help="RAW folder (two-folder mode)")
    parser.add_argument(
        "--anchor",
        choices=["jpg", "raw", "both"],
        default="jpg",
        help="Comparison method (default: jpg = list orphan RAWs)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete orphaned files (otherwise dry-run).",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the Mac app instead of running the CLI.",
    )
    args = parser.parse_args()

    if args.gui:
        from photopick.ui.app import main as gui_main

        return gui_main()

    if args.directory:
        jpgs, raws = scan_one_folder(Path(args.directory))
    elif args.jpg_dir and args.raw_dir:
        jpgs, raws = scan_two_folders(Path(args.jpg_dir), Path(args.raw_dir))
    else:
        parser.error("Provide a directory, or both --jpg-dir and --raw-dir, or --gui.")

    method = {
        "jpg": ComparisonMethod.ANCHOR_JPG,
        "raw": ComparisonMethod.ANCHOR_RAW,
        "both": ComparisonMethod.BOTH,
    }[args.anchor]

    result = classify(jpgs, raws, method)

    print(f"JPGs: {result.jpg_count}    RAWs: {result.raw_count}")
    print(f"Orphans: {len(result.orphans)}")
    for entry in result.orphans:
        tag = entry.side.upper()
        print(f"  [{tag}, missing {entry.missing_side.upper()}] {entry.path}")

    if args.execute and result.orphans:
        confirm = input(f"\nDelete {len(result.orphans)} file(s)? (yes/no): ")
        if confirm.strip().lower() != "yes":
            print("Cancelled.")
            return 0
        for entry in result.orphans:
            try:
                entry.path.unlink()
                print(f"Deleted: {entry.path}")
            except OSError as e:
                print(f"Failed: {entry.path} ({e})", file=sys.stderr)
    elif result.orphans:
        print("\n(Dry-run — pass --execute to delete.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
