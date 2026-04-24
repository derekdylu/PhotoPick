"""Main window — left sidebar feature switcher + content stack."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmapCache
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core import thumbs
from .inbox_view import InboxView
from .orphans_view import OrphansView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PhotoPick")
        self.setUnifiedTitleAndToolBarOnMac(True)

        central = QWidget(self)
        central.setObjectName("central")
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_sidebar(), 0)

        self.stack = QStackedWidget()
        self.orphans_view = OrphansView()
        self.inbox_view = InboxView()
        self.stack.addWidget(self.orphans_view)
        self.stack.addWidget(self.inbox_view)
        layout.addWidget(self.stack, 1)

        self.feature_list.setCurrentRow(0)

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar.setAttribute(Qt.WA_StyledBackground, True)

        v = QVBoxLayout(sidebar)
        v.setContentsMargins(14, 18, 14, 14)
        v.setSpacing(10)

        title = QLabel("PhotoPick")
        title.setObjectName("sidebarTitle")
        v.addWidget(title)

        self.feature_list = QListWidget()
        self.feature_list.setObjectName("featureList")
        self.feature_list.setFrameShape(QFrame.NoFrame)
        self.feature_list.addItem(QListWidgetItem("Remove Orphans"))
        self.feature_list.addItem(QListWidgetItem("Inbox Tray"))
        self.feature_list.currentRowChanged.connect(self._on_feature_changed)
        v.addWidget(self.feature_list, 1)

        self.cache_label = QLabel()
        self.cache_label.setObjectName("cacheLabel")
        self._refresh_cache_label()
        v.addWidget(self.cache_label)

        clear_btn = QPushButton("Clear cache")
        clear_btn.clicked.connect(self._on_clear_cache)
        v.addWidget(clear_btn)

        return sidebar

    def _on_feature_changed(self, row: int) -> None:
        if 0 <= row < self.stack.count():
            self.stack.setCurrentIndex(row)

    def _refresh_cache_label(self) -> None:
        size = thumbs.cache_size_bytes()
        if size < 1024:
            text = f"Cache: {size} B"
        elif size < 1024 * 1024:
            text = f"Cache: {size / 1024:.1f} KB"
        else:
            text = f"Cache: {size / (1024 * 1024):.1f} MB"
        self.cache_label.setText(text)

    def _on_clear_cache(self) -> None:
        deleted = thumbs.clear_cache()
        QPixmapCache.clear()
        self._refresh_cache_label()
        QMessageBox.information(
            self,
            "Cache cleared",
            f"Removed {deleted} cached thumbnail{'s' if deleted != 1 else ''}.",
        )
