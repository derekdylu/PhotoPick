"""Feature 2 — JPG inbox tray with Lightroom drag bridge."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QMimeData, QSize, Qt, QUrl
from PySide6.QtGui import QDrag, QIcon, QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core import thumbs
from ..core.matcher import find_raw_for_jpg, is_jpg
from ..core.scanner import scan_one_folder

PAYLOAD_RAW = "raw"
PAYLOAD_JPG = "jpg"
PAYLOAD_BOTH = "both"

_ROLE_JPG = Qt.UserRole + 1
_ROLE_RAW = Qt.UserRole + 2  # may be None


class InboxList(QListWidget):
    """A list that accepts dropped JPGs and drags out matched RAWs."""

    def __init__(self, owner: "InboxView") -> None:
        super().__init__()
        self.owner = owner
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(160, 120))
        self.setGridSize(QSize(180, 170))
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSpacing(8)
        self.setUniformItemSizes(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDefaultDropAction(Qt.CopyAction)
        self.setDropIndicatorShown(True)

    # --- drop-in -------------------------------------------------------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        added = 0
        for url in urls:
            if not url.isLocalFile():
                continue
            p = Path(url.toLocalFile())
            if p.is_file() and is_jpg(p):
                self.owner.add_jpg(p)
                added += 1
        if added:
            event.acceptProposedAction()
        else:
            event.ignore()

    # --- drag-out ------------------------------------------------------
    def startDrag(self, supportedActions):
        items = self.selectedItems()
        if not items:
            return

        urls = self.owner.build_drag_payload(items)
        if not urls:
            return

        mime = QMimeData()
        mime.setUrls(urls)

        drag = QDrag(self)
        drag.setMimeData(mime)

        first_pix = items[0].icon().pixmap(self.iconSize())
        if not first_pix.isNull():
            drag.setPixmap(first_pix)
            drag.setHotSpot(first_pix.rect().center())

        drag.exec(Qt.CopyAction)


class InboxView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.raw_folder: Path | None = None
        self._raw_index: dict[str, list[Path]] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        root.addWidget(self._build_setup())

        hint = QLabel(
            "Drag JPGs from Finder onto the tray below. "
            "Then select tiles and drag them onto Lightroom — "
            "the matched RAW(s) will be sent over."
        )
        hint.setStyleSheet("color: #888;")
        hint.setWordWrap(True)
        root.addWidget(hint)

        self.list_widget = InboxList(self)
        root.addWidget(self.list_widget, 1)

        root.addWidget(self._build_footer())

    def _build_setup(self) -> QWidget:
        box = QWidget()
        layout = QGridLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(6)

        layout.addWidget(QLabel("RAW source folder:"), 0, 0)
        self.raw_path_label = QLabel("(none)")
        self.raw_path_label.setStyleSheet("color: #555;")
        raw_btn = QPushButton("Choose…")
        raw_btn.clicked.connect(self._pick_raw_folder)
        layout.addWidget(self.raw_path_label, 0, 1)
        layout.addWidget(raw_btn, 0, 2)

        layout.addWidget(QLabel("Drag-out payload:"), 1, 0)
        self.payload_combo = QComboBox()
        self.payload_combo.addItem("RAW only (default)", PAYLOAD_RAW)
        self.payload_combo.addItem("JPG only", PAYLOAD_JPG)
        self.payload_combo.addItem("Both JPG + RAW", PAYLOAD_BOTH)
        layout.addWidget(self.payload_combo, 1, 1, 1, 2)

        layout.setColumnStretch(1, 1)
        return box

    def _build_footer(self) -> QWidget:
        box = QWidget()
        layout = QHBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)

        self.status_label = QLabel("0 in tray")
        self.status_label.setStyleSheet("color: #666;")
        layout.addWidget(self.status_label)

        layout.addStretch(1)

        clear_btn = QPushButton("Clear inbox")
        clear_btn.clicked.connect(self._clear_inbox)
        layout.addWidget(clear_btn)

        return box

    # --- raw folder ----------------------------------------------------
    def _pick_raw_folder(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Choose RAW source folder")
        if not path:
            return
        self.raw_folder = Path(path)
        self.raw_path_label.setText(path)
        self._rebuild_raw_index()
        self._rematch_all()

    def _rebuild_raw_index(self) -> None:
        self._raw_index.clear()
        if not self.raw_folder:
            return
        _, raws = scan_one_folder(self.raw_folder)
        for raw in raws:
            self._raw_index.setdefault(raw.stem.lower(), []).append(raw)

    # --- tile management ----------------------------------------------
    def add_jpg(self, jpg: Path) -> None:
        # Skip duplicates.
        for i in range(self.list_widget.count()):
            existing: Path = self.list_widget.item(i).data(_ROLE_JPG)
            if existing == jpg:
                return

        raw = find_raw_for_jpg(jpg, self._raw_index) if self._raw_index else None

        item = QListWidgetItem()
        item.setText(jpg.name + ("\n✓ RAW" if raw else "\n⚠ no RAW"))
        item.setToolTip(self._tile_tooltip(jpg, raw))
        item.setData(_ROLE_JPG, jpg)
        item.setData(_ROLE_RAW, raw)
        item.setIcon(self._load_icon(jpg))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.list_widget.addItem(item)
        self._update_status()

    def _tile_tooltip(self, jpg: Path, raw: Path | None) -> str:
        lines = [str(jpg)]
        if raw:
            lines.append(f"RAW: {raw}")
        else:
            lines.append("RAW: (no match in configured folder)")
        return "\n".join(lines)

    def _load_icon(self, jpg: Path) -> QIcon:
        data = thumbs.get_thumb_bytes(jpg)
        if data is None:
            return QIcon()
        pix = QPixmap()
        if not pix.loadFromData(data):
            return QIcon()
        return QIcon(pix)

    def _rematch_all(self) -> None:
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            jpg: Path = item.data(_ROLE_JPG)
            raw = find_raw_for_jpg(jpg, self._raw_index) if self._raw_index else None
            item.setData(_ROLE_RAW, raw)
            item.setText(jpg.name + ("\n✓ RAW" if raw else "\n⚠ no RAW"))
            item.setToolTip(self._tile_tooltip(jpg, raw))
        self._update_status()

    def _clear_inbox(self) -> None:
        self.list_widget.clear()
        self._update_status()

    def _update_status(self) -> None:
        total = self.list_widget.count()
        matched = sum(
            1
            for i in range(total)
            if self.list_widget.item(i).data(_ROLE_RAW) is not None
        )
        missing = total - matched
        self.status_label.setText(
            f"{total} in tray · {matched} RAW match{'es' if matched != 1 else ''} · {missing} missing"
        )

    # --- drag payload --------------------------------------------------
    def build_drag_payload(self, items: list[QListWidgetItem]) -> list[QUrl]:
        mode = self.payload_combo.currentData()
        urls: list[QUrl] = []
        for item in items:
            jpg: Path = item.data(_ROLE_JPG)
            raw: Path | None = item.data(_ROLE_RAW)
            if mode == PAYLOAD_JPG:
                urls.append(QUrl.fromLocalFile(str(jpg)))
            elif mode == PAYLOAD_RAW:
                if raw is not None:
                    urls.append(QUrl.fromLocalFile(str(raw)))
            elif mode == PAYLOAD_BOTH:
                urls.append(QUrl.fromLocalFile(str(jpg)))
                if raw is not None:
                    urls.append(QUrl.fromLocalFile(str(raw)))
        return urls
