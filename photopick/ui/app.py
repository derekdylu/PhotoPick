"""QApplication entrypoint for the PhotoPick Mac app."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow
from .styles import apply_app_style

_ICON_PATH = Path(__file__).resolve().parents[2] / "assets" / "PhotoPick.png"


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoPick")
    app.setOrganizationName("PhotoPick")
    app.setOrganizationDomain("photoPick.local")
    if _ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(_ICON_PATH)))
    apply_app_style(app)

    window = MainWindow()
    window.resize(1180, 760)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
