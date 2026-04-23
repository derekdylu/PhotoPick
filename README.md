# RAW Organizer

A macOS app (with a CLI fallback) for managing RAW + JPG photo pairs.

Two features:

1. **Remove Orphans** — find and delete RAW/JPG files that are missing their counterpart.
2. **Inbox Tray → Lightroom** — drop JPGs you like onto a tray, then drag the matched RAW(s) straight into Lightroom.

Plus a global **Clear cache** action for thumbnail previews.

---

## The Mac app

### Run from source

```bash
pip install -r requirements.txt
python -m raw_organizer.ui.app
# or:
python raw_organizer.py --gui
```

### Build a `.app` bundle

```bash
pip install briefcase
briefcase create macOS
briefcase build macOS
briefcase package macOS --no-sign      # for local use
# or briefcase package macOS            # signed/notarised release
```

The bundle ends up under `macOS/app/Raw Organizer/`.

### Feature 1 — Remove Orphans

- **Mode**: `Single folder` (RAW + JPG mixed) or `Two folders` (RAW and JPG in separate dirs).
- **Comparison method**:
  - `Anchor JPG` — list RAW files with no matching JPG.
  - `Anchor RAW` — list JPG files with no matching RAW.
  - `Both` — list anything missing its counterpart.
- The orphan list shows filenames only. **Previews are loaded only when you click a row** — scrolling thousands of files costs nothing.
- `Reveal in Finder` and `Move to Trash` (uses macOS Trash via `send2trash` — never a permanent delete).

### Feature 2 — Inbox Tray

- Pick a **RAW source folder**. The tray will look up matching RAWs by basename whenever you drop a JPG.
- **Drag JPGs in** from Finder, Preview, browsers, anywhere — tiles appear, badged `✓ RAW` or `⚠ no RAW`.
- **Multi-select**, then drag the tiles **out onto Lightroom** (the import window or a watched folder).
- The drag payload is configurable:
  - `RAW only` (default) — only the matched RAWs go to Lightroom. JPGs without a match are silently skipped.
  - `JPG only` — just the JPGs.
  - `Both` — both files of each pair.

### Clear cache

Removes `~/Library/Caches/RawOrganizer/thumbs/`. The next preview re-decodes from source.

---

## Supported file types

**JPG**: `.jpg`, `.jpeg`
**RAW**: `.cr2`, `.cr3`, `.nef`, `.arw`, `.dng`, `.orf`, `.rw2`, `.pef`, `.srw`, `.x3f`

---

## CLI

The original CLI still works (no third-party deps for the CLI alone — `PySide6`/`rawpy`/etc. are only needed for the GUI):

```bash
# Single folder, anchor on JPG (default)
python raw_organizer.py /path/to/photos

# Single folder, find orphans both directions
python raw_organizer.py /path/to/photos --anchor both

# Two-folder mode
python raw_organizer.py --jpg-dir /path/jpg --raw-dir /path/raw --anchor raw

# Actually delete (otherwise dry-run)
python raw_organizer.py /path/to/photos --execute

# Launch the Mac app
python raw_organizer.py --gui
```

---

## License

MIT
