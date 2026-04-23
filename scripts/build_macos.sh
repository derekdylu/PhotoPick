#!/usr/bin/env bash
# Build a Raw Organizer .app bundle and .dmg installer.
#
# Uses PyInstaller for the .app bundle (most reliable for PySide6 + rawpy)
# and hdiutil for the .dmg (no extra Homebrew deps required).
#
# Usage:
#   ./scripts/build_macos.sh                # build .app + .dmg, ad-hoc signed
#   ./scripts/build_macos.sh --sign IDENT   # sign with Developer ID "IDENT"
#
# Output:
#   dist/Raw Organizer.app
#   dist/Raw-Organizer-<version>.dmg

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

VERSION="$(/usr/bin/grep -E '^version' pyproject.toml | head -1 | /usr/bin/sed -E 's/.*"([^"]+)".*/\1/')"
APP_NAME="Raw Organizer"
DMG_NAME="Raw-Organizer-${VERSION}"

# --- pick a Python 3.10+ interpreter --------------------------------------
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    ver=$("$candidate" -c 'import sys; print("%d.%d" % sys.version_info[:2])')
    major=${ver%.*}; minor=${ver#*.}
    if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
      PYTHON="$candidate"
      break
    fi
  fi
done

if [ -z "$PYTHON" ]; then
  echo "Error: need Python 3.10+. Install with: brew install python@3.13" >&2
  exit 1
fi

echo "Using $PYTHON ($(command -v "$PYTHON"))"

# --- venv with PyInstaller + app deps -------------------------------------
VENV="$PROJECT_ROOT/.venv-build"
if [ ! -d "$VENV" ]; then
  echo "Creating build venv at $VENV"
  "$PYTHON" -m venv "$VENV"
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

pip install --upgrade pip wheel >/dev/null
pip install --upgrade \
    "pyinstaller>=6.6" \
    "PySide6>=6.6" \
    "rawpy>=0.19" \
    "Pillow>=10.0" \
    "send2trash>=1.8"

# --- clean previous build -------------------------------------------------
rm -rf build "dist/${APP_NAME}.app" "dist/${DMG_NAME}.dmg" "dist/${APP_NAME}"

# --- PyInstaller ----------------------------------------------------------
echo "==> pyinstaller"
EXCLUDES=(
    PySide6.Qt3DAnimation PySide6.Qt3DCore PySide6.Qt3DExtras PySide6.Qt3DInput
    PySide6.Qt3DLogic PySide6.Qt3DRender PySide6.QtAsyncio PySide6.QtBluetooth
    PySide6.QtCanvasPainter PySide6.QtCharts PySide6.QtConcurrent PySide6.QtDBus
    PySide6.QtDataVisualization PySide6.QtDesigner PySide6.QtGraphs
    PySide6.QtGraphsWidgets PySide6.QtHelp PySide6.QtHttpServer
    PySide6.QtLocation PySide6.QtMultimedia PySide6.QtMultimediaWidgets
    PySide6.QtNetworkAuth PySide6.QtNfc PySide6.QtOpenGL PySide6.QtOpenGLWidgets
    PySide6.QtPdf PySide6.QtPdfWidgets PySide6.QtPositioning
    PySide6.QtPrintSupport PySide6.QtQml PySide6.QtQuick PySide6.QtQuick3D
    PySide6.QtQuickControls2 PySide6.QtQuickTest PySide6.QtQuickWidgets
    PySide6.QtRemoteObjects PySide6.QtScxml PySide6.QtSensors PySide6.QtSerialBus
    PySide6.QtSerialPort PySide6.QtSpatialAudio PySide6.QtSql
    PySide6.QtStateMachine PySide6.QtSvg PySide6.QtSvgWidgets PySide6.QtTest
    PySide6.QtTextToSpeech PySide6.QtUiTools PySide6.QtWebChannel
    PySide6.QtWebEngineCore PySide6.QtWebEngineQuick PySide6.QtWebEngineWidgets
    PySide6.QtWebSockets PySide6.QtWebView PySide6.QtXml
    PySide6.scripts PySide6.scripts.deploy PySide6.scripts.deploy_lib
    PySide6.scripts.android_deploy PySide6.scripts.metaobjectdump
    PySide6.scripts.project PySide6.scripts.project_lib
    PySide6.scripts.pyside_tool PySide6.scripts.qml PySide6.scripts.qtpy2cpp
    PySide6.support.deprecated PySide6.support.generate_pyi
)
EXCLUDE_ARGS=()
for e in "${EXCLUDES[@]}"; do EXCLUDE_ARGS+=(--exclude-module "$e"); done

pyinstaller \
    --windowed \
    --noconfirm \
    --name "$APP_NAME" \
    --osx-bundle-identifier "local.rawOrganizer" \
    "${EXCLUDE_ARGS[@]}" \
    --hidden-import PySide6.QtCore \
    --hidden-import PySide6.QtGui \
    --hidden-import PySide6.QtWidgets \
    --hidden-import rawpy \
    --hidden-import PIL.Image \
    --hidden-import send2trash \
    --paths "$PROJECT_ROOT" \
    --collect-submodules raw_organizer \
    "$PROJECT_ROOT/scripts/_launcher.py"

APP_BUNDLE="dist/${APP_NAME}.app"
if [ ! -d "$APP_BUNDLE" ]; then
  echo "Error: expected $APP_BUNDLE to exist after pyinstaller" >&2
  exit 1
fi

# --- ad-hoc / Developer ID code-sign --------------------------------------
if [ "${1:-}" = "--sign" ] && [ -n "${2:-}" ]; then
  echo "==> codesign with identity: $2"
  codesign --deep --force --options runtime --sign "$2" "$APP_BUNDLE"
else
  echo "==> ad-hoc codesign"
  codesign --deep --force --sign - "$APP_BUNDLE"
fi

# --- DMG ------------------------------------------------------------------
DMG_PATH="dist/${DMG_NAME}.dmg"
echo "==> building DMG: $DMG_PATH"

STAGING="$(mktemp -d)"
cp -R "$APP_BUNDLE" "$STAGING/"
ln -s /Applications "$STAGING/Applications"

hdiutil create \
    -volname "$APP_NAME" \
    -srcfolder "$STAGING" \
    -ov -format UDZO \
    "$DMG_PATH"

rm -rf "$STAGING"

# --- summary --------------------------------------------------------------
echo
echo "Build complete."
echo "  .app: $PROJECT_ROOT/$APP_BUNDLE"
echo "  .dmg: $PROJECT_ROOT/$DMG_PATH"

if [ "${1:-}" != "--sign" ]; then
  echo
  echo "Note: this build is ad-hoc signed (not notarised). To open it the"
  echo "first time on a Mac, right-click the .app and choose Open, or run:"
  echo "    xattr -dr com.apple.quarantine \"/Applications/${APP_NAME}.app\""
fi
