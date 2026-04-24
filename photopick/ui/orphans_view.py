"""Feature 1 — find and clean up orphaned JPG/RAW files."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QPixmap
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
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ..core import thumbs
from ..core.matcher import ComparisonMethod, classify
from ..core.scanner import scan_one_folder, scan_two_folders


class OrphansView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.jpg_folder: Path | None = None
        self.raw_folder: Path | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 20)
        root.setSpacing(16)

        root.addWidget(self._build_setup())

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.setHandleWidth(8)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_widget.currentItemChanged.connect(self._on_selection_changed)
        splitter.addWidget(self.list_widget)

        self.preview_label = QLabel("Select a file to preview")
        self.preview_label.setObjectName("preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumWidth(360)
        self.preview_label.setAttribute(Qt.WA_StyledBackground, True)
        splitter.addWidget(self.preview_label)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        root.addWidget(splitter, 1)

        root.addWidget(self._build_actions())

        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        root.addWidget(self.status_label)

    def _build_setup(self) -> QWidget:
        box = QWidget()
        layout = QGridLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(16)

        layout.addWidget(QLabel("Mode:"), 0, 0)
        self.single_radio = QRadioButton("Single folder (mixed)")
        self.two_radio = QRadioButton("Two folders (separate)")
        self.single_radio.setChecked(True)
        mode_group = QButtonGroup(self)
        mode_group.addButton(self.single_radio)
        mode_group.addButton(self.two_radio)
        self.single_radio.toggled.connect(self._update_pickers)
        layout.addWidget(self.single_radio, 0, 1)
        layout.addWidget(self.two_radio, 0, 2)

        self.jpg_label = QLabel("JPG folder:")
        self.jpg_path_label = QLabel("(none)")
        self.jpg_path_label.setStyleSheet("color: #555;")
        jpg_btn = QPushButton("Choose…")
        jpg_btn.clicked.connect(self._pick_jpg_folder)
        layout.addWidget(self.jpg_label, 1, 0)
        layout.addWidget(self.jpg_path_label, 1, 1, 1, 2)
        layout.addWidget(jpg_btn, 1, 3)

        self.raw_label = QLabel("RAW folder:")
        self.raw_path_label = QLabel("(none)")
        self.raw_path_label.setStyleSheet("color: #555;")
        self.raw_btn = QPushButton("Choose…")
        self.raw_btn.clicked.connect(self._pick_raw_folder)
        layout.addWidget(self.raw_label, 2, 0)
        layout.addWidget(self.raw_path_label, 2, 1, 1, 2)
        layout.addWidget(self.raw_btn, 2, 3)

        layout.addWidget(QLabel("Method:"), 3, 0)
        self.method_combo = QComboBox()
        self.method_combo.addItem("Anchor JPG (find orphan RAWs)", ComparisonMethod.ANCHOR_JPG)
        self.method_combo.addItem("Anchor RAW (find orphan JPGs)", ComparisonMethod.ANCHOR_RAW)
        self.method_combo.addItem("Both (symmetric)", ComparisonMethod.BOTH)
        layout.addWidget(self.method_combo, 3, 1, 1, 2)

        scan_btn = QPushButton("Scan")
        scan_btn.setDefault(True)
        scan_btn.clicked.connect(self._on_scan)
        layout.addWidget(scan_btn, 3, 3)

        self._update_pickers()
        return box

    def _build_actions(self) -> QWidget:
        box = QWidget()
        layout = QHBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        reveal_btn = QPushButton("Reveal in Finder")
        reveal_btn.clicked.connect(self._reveal_selected)
        layout.addWidget(reveal_btn)

        trash_btn = QPushButton("Move selected to Trash")
        trash_btn.clicked.connect(self._trash_selected)
        layout.addWidget(trash_btn)

        trash_all_btn = QPushButton("Move ALL listed to Trash")
        trash_all_btn.clicked.connect(self._trash_all)
        layout.addWidget(trash_all_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear_results)
        layout.addWidget(clear_btn)

        layout.addStretch(1)
        return box

    def _clear_results(self) -> None:
        self.list_widget.clear()
        self.preview_label.clear()
        self.preview_label.setText("Select a file to preview")
        self.status_label.setText("")

    def _update_pickers(self) -> None:
        single = self.single_radio.isChecked()
        if single:
            self.jpg_label.setText("Folder:")
            self.raw_label.setVisible(False)
            self.raw_path_label.setVisible(False)
            self.raw_btn.setVisible(False)
        else:
            self.jpg_label.setText("JPG folder:")
            self.raw_label.setText("RAW folder:")
            self.raw_label.setVisible(True)
            self.raw_path_label.setVisible(True)
            self.raw_btn.setVisible(True)

    def _pick_jpg_folder(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Choose folder")
        if path:
            self.jpg_folder = Path(path)
            self.jpg_path_label.setText(path)

    def _pick_raw_folder(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Choose RAW folder")
        if path:
            self.raw_folder = Path(path)
            self.raw_path_label.setText(path)

    def _on_scan(self) -> None:
        single = self.single_radio.isChecked()
        if single:
            if not self.jpg_folder:
                QMessageBox.warning(self, "Pick a folder", "Choose a folder to scan first.")
                return
            jpgs, raws = scan_one_folder(self.jpg_folder)
        else:
            if not self.jpg_folder or not self.raw_folder:
                QMessageBox.warning(self, "Pick folders", "Choose both JPG and RAW folders.")
                return
            jpgs, raws = scan_two_folders(self.jpg_folder, self.raw_folder)

        method: ComparisonMethod = self.method_combo.currentData()
        result = classify(jpgs, raws, method)

        self.list_widget.clear()
        for entry in result.orphans:
            tag = "RAW" if entry.side == "raw" else "JPG"
            label = f"[{tag}, missing {entry.missing_side.upper()}]  {entry.path.name}"
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, entry.path)
            item.setToolTip(str(entry.path))
            self.list_widget.addItem(item)

        self.status_label.setText(
            f"Scanned {result.jpg_count} JPGs, {result.raw_count} RAWs — "
            f"{len(result.orphans)} orphan{'s' if len(result.orphans) != 1 else ''} found."
        )
        self.preview_label.clear()
        self.preview_label.setText("Select a file to preview")

    def _on_selection_changed(self, current: QListWidgetItem | None, _prev) -> None:
        if current is None:
            self.preview_label.clear()
            self.preview_label.setText("Select a file to preview")
            return
        path: Path = current.data(Qt.UserRole)
        self.preview_label.setText(f"Loading {path.name}…")
        self.preview_label.repaint()
        data = thumbs.get_thumb_bytes(path)
        if data is None:
            self.preview_label.setText(f"No preview available for\n{path.name}")
            return
        pix = QPixmap()
        if not pix.loadFromData(data):
            self.preview_label.setText(f"Could not decode preview for\n{path.name}")
            return
        scaled = pix.scaled(
            self.preview_label.size() - QSize(20, 20),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.preview_label.setPixmap(scaled)

    def _reveal_selected(self) -> None:
        item = self.list_widget.currentItem()
        if item is None:
            return
        path: Path = item.data(Qt.UserRole)
        subprocess.run(["open", "-R", str(path)], check=False)

    def _trash_selected(self) -> None:
        item = self.list_widget.currentItem()
        if item is None:
            return
        path: Path = item.data(Qt.UserRole)
        if QMessageBox.question(
            self,
            "Move to Trash",
            f"Move this file to the Trash?\n\n{path}",
        ) != QMessageBox.Yes:
            return
        if self._send_to_trash([path]) > 0:
            self.list_widget.takeItem(self.list_widget.row(item))

    def _trash_all(self) -> None:
        if self.list_widget.count() == 0:
            return
        if QMessageBox.question(
            self,
            "Move all to Trash",
            f"Move all {self.list_widget.count()} listed files to the Trash?",
        ) != QMessageBox.Yes:
            return
        paths = [
            self.list_widget.item(i).data(Qt.UserRole)
            for i in range(self.list_widget.count())
        ]
        moved = self._send_to_trash(paths)
        self.list_widget.clear()
        QMessageBox.information(self, "Done", f"Moved {moved} file(s) to Trash.")

    def _send_to_trash(self, paths: list[Path]) -> int:
        try:
            from send2trash import send2trash
        except ImportError:
            QMessageBox.critical(
                self,
                "Missing dependency",
                "send2trash is not installed. Install with: pip install send2trash",
            )
            return 0
        moved = 0
        for p in paths:
            try:
                send2trash(str(p))
                moved += 1
            except Exception as e:  # noqa: BLE001
                QMessageBox.warning(self, "Trash failed", f"{p}\n\n{e}")
        return moved
