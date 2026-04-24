<div align="center">

<img src="assets/hero.jpg" alt="PhotoPick" width="100%" />

# PhotoPick

**A macOS app for managing RAW + JPG photo pairs and pushing picks into Lightroom or another folder.**

</div>

---

## What it does

1. **Remove Orphans** — find (and optionally trash) RAW or JPG files that are missing their counterpart.
2. **Inbox Tray → Lightroom or another folder** — drop the JPGs you like onto a tray, then drag the matched RAW(s) straight into Lightroom or another folder.
3. A global **Clear cache** action for thumbnail previews.

Works on RAW from Canon, Nikon, Sony, Fuji, Pentax, Panasonic, Sigma, Olympus, and Adobe (`.cr2` `.cr3` `.nef` `.arw` `.dng` `.orf` `.rw2` `.pef` `.srw` `.x3f`), paired against `.jpg` / `.jpeg`.

---

## Install

Pre-built `.dmg` releases will be published on the [**GitHub Releases**](https://github.com/derekdylu/PhotoPick/releases) page. Until then, build from source — it's one command.

### Build from source

```bash
git clone https://github.com/derekdylu/PhotoPick.git
cd PhotoPick
./scripts/build_macos.sh
```

This produces:

- `dist/PhotoPick.app` — the bundled macOS app (~120 MB)
- `dist/PhotoPick-<version>.dmg` — a draggable installer (~50 MB)

First build takes ~3 min (most of it downloading PySide6 wheels); incremental rebuilds are ~30 s.

**Requirements**
- macOS (Apple Silicon or Intel)
- Python 3.10+ — the script auto-detects `python3.10`–`python3.13`; install with `brew install python@3.13` if you don't have one
- Xcode Command Line Tools (`xcode-select --install`)

### Run from source (no build)

```bash
pip install -r requirements.txt
python -m photopick.ui.app
# or
python photopick.py --gui
```

---

## First launch — "PhotoPick is damaged" / "is malware" warning

PhotoPick is ad-hoc signed and **not** notarised by Apple. The first time you
open it, macOS (especially Sequoia 15.x) will likely show:

> "PhotoPick" is damaged and can't be opened. You should move it to the Trash.

This is **not** because the app is actually malicious — it's Gatekeeper's
default reaction to any app that lacks an Apple-issued signature and carries
the quarantine flag set by Safari/Finder on download. Builds you produced
yourself and downloads from this project's Releases both land in this state.

Pick either fix below — you only need to do it once.

### Option A — Terminal (one command)

```bash
# App is in /Applications
sudo xattr -dr com.apple.quarantine /Applications/PhotoPick.app

# App is still in ~/Downloads
xattr -dr com.apple.quarantine ~/Downloads/PhotoPick.app
```

Then double-click PhotoPick normally.

### Option B — GUI (no Terminal)

1. Double-click PhotoPick so the "is damaged" / "is malware" dialog appears,
   then click **Cancel** (do **not** click "Move to Trash").
2. Open **System Settings → Privacy & Security**.
3. Scroll to the **Security** section. You'll see a line like
   *"PhotoPick was blocked to protect your Mac."*
4. Click **Open Anyway** next to it. Authenticate with Touch ID or your
   password.
5. Launch PhotoPick again — confirm **Open** in the follow-up dialog.

> macOS Sequoia note: the old "right-click → Open" workaround **no longer
> works**. The damaged/malware dialog in Sequoia only shows a "Move to Trash"
> button, so you must use Option A or Option B above.

### Developer ID signing (optional)

```bash
./scripts/build_macos.sh --sign "Developer ID Application: Your Name (TEAMID)"
xcrun notarytool submit dist/PhotoPick-<version>.dmg --apple-id ... --wait
```

---

## Features

### Remove Orphans

<p align="center"><img src="assets/screenshots/orphans.jpg" alt="Remove Orphans view" width="720" /></p>

- **Mode**: *Single folder* (RAW + JPG mixed) or *Two folders* (RAW and JPG separate).
- **Comparison**:
  - `Anchor JPG` — RAWs with no matching JPG
  - `Anchor RAW` — JPGs with no matching RAW
  - `Both` — anything missing its counterpart
- The orphan list shows filenames only. Previews are loaded lazily on click — scrolling thousands of files costs nothing.
- `Reveal in Finder` and `Move to Trash` (via `send2trash` — never a permanent delete).

### Inbox Tray

<p align="center"><img src="assets/screenshots/inbox.jpg" alt="Inbox Tray view" width="720" /></p>

- Pick a **RAW source folder**. Every dropped JPG is looked up by basename.
- **Drag JPGs in** from Finder, Preview, browsers, etc. Tiles are badged `✓ RAW` or `⚠ no RAW`.
- **Multi-select + drag out** onto Lightroom (import window or a watched folder).
- Configurable drag payload:
  - `RAW only` (default) — just the matched RAWs
  - `JPG only`
  - `Both`

### Clear cache

Removes `~/Library/Caches/PhotoPick/thumbs/`. Next preview re-decodes from source.

---

## CLI

No third-party deps for the CLI alone — `PySide6` / `rawpy` / etc. are only needed for the GUI.

```bash
# Single folder, anchor on JPG (default)
python photopick.py /path/to/photos

# Find orphans both directions
python photopick.py /path/to/photos --anchor both

# Two-folder mode
python photopick.py --jpg-dir /path/jpg --raw-dir /path/raw --anchor raw

# Actually delete (otherwise dry-run)
python photopick.py /path/to/photos --execute

# Launch the Mac app
python photopick.py --gui
```

---

## Repo layout

```
photopick/               # Python package
├── core/                # Pure-Python scanner/matcher/thumbs (no GUI deps)
│   ├── matcher.py
│   ├── scanner.py
│   └── thumbs.py
└── ui/                  # PySide6 Mac app
    ├── app.py
    ├── main_window.py
    ├── inbox_view.py
    ├── orphans_view.py
    └── styles.py

scripts/
├── build_macos.sh       # One-shot .app + .dmg build
└── _launcher.py         # PyInstaller entry point

PhotoPick.spec           # PyInstaller spec
assets/PhotoPick.icns    # App icon
```

---

## License

[MIT](LICENSE) © Derek Lu
