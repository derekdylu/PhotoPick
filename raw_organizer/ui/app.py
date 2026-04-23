"""QApplication entrypoint for the Raw Organizer Mac app."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from .main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Raw Organizer")
    app.setOrganizationName("Raw Organizer")
    app.setOrganizationDomain("rawOrganizer.local")

    window = MainWindow()
    window.resize(1100, 720)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
