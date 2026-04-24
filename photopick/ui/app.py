"""QApplication entrypoint for the Raw Organizer Mac app."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from .main_window import MainWindow
from .styles import apply_app_style


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Raw Organizer")
    app.setOrganizationName("Raw Organizer")
    app.setOrganizationDomain("rawOrganizer.local")
    apply_app_style(app)

    window = MainWindow()
    window.resize(1180, 760)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
