"""Feature 2 — JPG inbox tray with Lightroom drag bridge."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QMimeData, QSize, Qt, QUrl
from PySide6.QtGui import QDrag, QIcon, QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..core import thumbs
from ..core.matcher import find_raw_for_jpg, is_jpg
from ..core.scanner import scan_one_folder
from .folder_drop_label import FolderDropLabel

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
        self.setIconSize(QSize(180, 135))
        self.setGridSize(QSize(204, 196))
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSpacing(10)
        self.setUniformItemSizes(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.viewport().setAcceptDrops(True)
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
        skipped_scope = 0
        for url in urls:
            if not url.isLocalFile():
                continue
            p = Path(url.toLocalFile())
            if not (p.is_file() and is_jpg(p)):
                continue
            if not self.owner.is_in_jpg_scope(p):
                skipped_scope += 1
                continue
            self.owner.add_jpg(p)
            added += 1
        if added:
            event.acceptProposedAction()
        else:
            event.ignore()
        if skipped_scope:
            self.owner.note_out_of_scope(skipped_scope)

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
        self.jpg_folder: Path | None = None
        self.raw_folder: Path | None = None
        self._raw_index: dict[str, list[Path]] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 20)
        root.setSpacing(16)

        root.addWidget(self._build_setup())

        self.hint_label = QLabel()
        self.hint_label.setObjectName("hint")
        self.hint_label.setWordWrap(True)
        root.addWidget(self.hint_label)

        self.list_widget = InboxList(self)
        root.addWidget(self.list_widget, 1)

        root.addWidget(self._build_footer())

        self._update_enabled()

    def _build_setup(self) -> QWidget:
        box = QWidget()
        layout = QGridLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(16)

        layout.addWidget(QLabel("Mode:"), 0, 0)
        self.single_radio = QRadioButton("Single folder (mixed)")
        self.two_radio = QRadioButton("Two folders (separate)")
        self.two_radio.setChecked(True)
        mode_group = QButtonGroup(self)
        mode_group.addButton(self.single_radio)
        mode_group.addButton(self.two_radio)
        self.single_radio.toggled.connect(self._update_pickers)
        layout.addWidget(self.single_radio, 0, 1)
        layout.addWidget(self.two_radio, 0, 2)

        self.jpg_source_label = QLabel("JPG source folder:")
        layout.addWidget(self.jpg_source_label, 1, 0)
        self.jpg_path_label = FolderDropLabel("(none)")
        self.jpg_path_label.folder_dropped.connect(self._set_jpg_folder)
        jpg_btn = QPushButton("Choose…")
        jpg_btn.clicked.connect(self._pick_jpg_folder)
        layout.addWidget(self.jpg_path_label, 1, 1)
        layout.addWidget(jpg_btn, 1, 2)

        self.raw_source_label = QLabel("RAW source folder:")
        layout.addWidget(self.raw_source_label, 2, 0)
        self.raw_path_label = FolderDropLabel("(none)")
        self.raw_path_label.folder_dropped.connect(self._set_raw_folder)
        self.raw_btn = QPushButton("Choose…")
        self.raw_btn.clicked.connect(self._pick_raw_folder)
        layout.addWidget(self.raw_path_label, 2, 1)
        layout.addWidget(self.raw_btn, 2, 2)

        layout.addWidget(QLabel("Drag-out payload:"), 3, 0)
        self.payload_combo = QComboBox()
        self.payload_combo.addItem("RAW only (default)", PAYLOAD_RAW)
        self.payload_combo.addItem("JPG only", PAYLOAD_JPG)
        self.payload_combo.addItem("Both JPG + RAW", PAYLOAD_BOTH)
        layout.addWidget(self.payload_combo, 3, 1, 1, 2)

        layout.setColumnStretch(1, 1)
        self._update_pickers()
        return box

    def _update_pickers(self) -> None:
        single = self.single_radio.isChecked()
        if single:
            self.jpg_source_label.setText("Folder:")
            self.raw_source_label.setVisible(False)
            self.raw_path_label.setVisible(False)
            self.raw_btn.setVisible(False)
            # Mirror JPG folder into RAW slot so matching uses the same folder.
            if self.jpg_folder is not None:
                self.raw_folder = self.jpg_folder
                self._rebuild_raw_index()
                self._rematch_all()
        else:
            self.jpg_source_label.setText("JPG source folder:")
            self.raw_source_label.setVisible(True)
            self.raw_path_label.setVisible(True)
            self.raw_btn.setVisible(True)
            # If RAW was mirrored from JPG in single-folder mode, require a fresh pick.
            if self.raw_folder is not None and self.raw_folder == self.jpg_folder and self.raw_path_label.text() == "(none)":
                self.raw_folder = None
                self._raw_index.clear()
                self._rematch_all()
        self._update_enabled()

    def _build_footer(self) -> QWidget:
        box = QWidget()
        layout = QHBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)

        self.status_label = QLabel("0 in tray")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)

        layout.addStretch(1)

        clear_btn = QPushButton("Clear inbox")
        clear_btn.clicked.connect(self._clear_inbox)
        layout.addWidget(clear_btn)

        return box

    # --- folder pickers ------------------------------------------------
    def _pick_jpg_folder(self) -> None:
        prompt = (
            "Choose folder"
            if self.single_radio.isChecked()
            else "Choose JPG source folder"
        )
        path = QFileDialog.getExistingDirectory(self, prompt)
        if not path:
            return
        self._set_jpg_folder(Path(path))

    def _pick_raw_folder(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Choose RAW source folder")
        if not path:
            return
        self._set_raw_folder(Path(path))

    def _set_jpg_folder(self, folder: Path) -> None:
        self.jpg_folder = folder
        self.jpg_path_label.setText(str(folder))
        if self.single_radio.isChecked():
            # In single-folder mode, RAWs live in the same folder.
            self.raw_folder = folder
            self._rebuild_raw_index()
            self._rematch_all()
        self._update_enabled()

    def _set_raw_folder(self, folder: Path) -> None:
        self.raw_folder = folder
        self.raw_path_label.setText(str(folder))
        self._rebuild_raw_index()
        self._rematch_all()
        self._update_enabled()

    def _ready(self) -> bool:
        if self.single_radio.isChecked():
            return self.jpg_folder is not None
        return self.jpg_folder is not None and self.raw_folder is not None

    def _update_enabled(self) -> None:
        # May be called during _build_setup, before list_widget exists.
        if not hasattr(self, "list_widget"):
            return
        ready = self._ready()
        self.list_widget.setEnabled(ready)
        if ready:
            self.hint_label.setText(
                "Drag JPGs from Finder onto the tray below. "
                "Then select tiles and drag them onto Lightroom — "
                "the matched RAW(s) will be sent over."
            )
        elif self.single_radio.isChecked():
            self.hint_label.setText(
                "Set the folder above (or drag a file onto the path) to enable the tray."
            )
        else:
            self.hint_label.setText(
                "Set both the JPG and RAW source folders above to enable the tray."
            )

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

    def _update_status(self, suffix: str = "") -> None:
        total = self.list_widget.count()
        matched = sum(
            1
            for i in range(total)
            if self.list_widget.item(i).data(_ROLE_RAW) is not None
        )
        missing = total - matched
        text = (
            f"{total} in tray · {matched} RAW match{'es' if matched != 1 else ''} · {missing} missing"
        )
        if suffix:
            text = f"{text} · {suffix}"
        self.status_label.setText(text)

    def is_in_jpg_scope(self, path: Path) -> bool:
        if self.jpg_folder is None:
            return False
        try:
            path.resolve().relative_to(self.jpg_folder.resolve())
            return True
        except ValueError:
            return False

    def note_out_of_scope(self, count: int) -> None:
        self._update_status(
            f"skipped {count} file{'s' if count != 1 else ''} outside JPG folder"
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
