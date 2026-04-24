"""QLabel subclass that accepts file/folder drops to designate a folder path."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent
from PySide6.QtWidgets import QLabel


_BASE_STYLE = "color: #555;"
_HOVER_STYLE = (
    "color: #1d4ed8;"
    "border: 1px dashed #1d4ed8;"
    "border-radius: 4px;"
    "padding: 2px 4px;"
)


class FolderDropLabel(QLabel):
    """Displays a path and emits `folder_dropped(Path)` when a file/folder is dropped on it.

    On drop, resolves the dropped URL's parent directory (or the URL itself if it's
    already a directory) and emits that path.
    """

    folder_dropped = Signal(Path)

    def __init__(self, text: str = "", parent=None) -> None:
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.setStyleSheet(_BASE_STYLE)

    def _has_local_url(self, event) -> bool:
        md = event.mimeData()
        if not md.hasUrls():
            return False
        return any(u.isLocalFile() for u in md.urls())

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if self._has_local_url(event):
            self.setStyleSheet(_HOVER_STYLE)
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if self._has_local_url(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        self.setStyleSheet(_BASE_STYLE)
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        self.setStyleSheet(_BASE_STYLE)
        for url in event.mimeData().urls():
            if not url.isLocalFile():
                continue
            p = Path(url.toLocalFile())
            folder = p if p.is_dir() else p.parent
            if folder.is_dir():
                self.folder_dropped.emit(folder)
                event.acceptProposedAction()
                return
        event.ignore()
