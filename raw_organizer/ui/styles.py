"""macOS 26 (Tahoe) inspired stylesheet.

Goal: rounded, padded, low-chrome look with a single accent color and the
system-typical "pill" selection in the sidebar. Auto-adapts to light/dark.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

ACCENT = "#0a84ff"
ACCENT_HOVER = "#0066d4"

_LIGHT = f"""
QWidget {{
    color: #1c1c1e;
    font-size: 13px;
}}

QMainWindow, QWidget#central, QStackedWidget, QStackedWidget > QWidget {{
    background-color: #f3f3f5;
}}

QWidget#sidebar {{
    background-color: #eaeaee;
    border: none;
}}

QLabel#sidebarTitle {{
    color: #1c1c1e;
    font-size: 15px;
    font-weight: 600;
    padding: 4px 8px 8px 8px;
}}

QLabel#cacheLabel {{
    color: #6c6c70;
    font-size: 11px;
    padding: 0 6px;
}}

QListWidget#featureList {{
    background: transparent;
    border: none;
    outline: none;
    padding: 0;
}}
QListWidget#featureList::item {{
    padding: 9px 12px;
    margin: 2px 0;
    border-radius: 9px;
    color: #1c1c1e;
}}
QListWidget#featureList::item:hover {{
    background-color: rgba(0, 0, 0, 0.05);
}}
QListWidget#featureList::item:selected {{
    background-color: {ACCENT};
    color: white;
}}

QPushButton {{
    background-color: white;
    border: 1px solid #d8d8dc;
    border-radius: 8px;
    padding: 6px 14px;
    color: #1c1c1e;
    min-height: 20px;
}}
QPushButton:hover {{
    background-color: #f7f7f9;
}}
QPushButton:pressed {{
    background-color: #ebebee;
}}
QPushButton:default {{
    background-color: {ACCENT};
    color: white;
    border: 1px solid transparent;
}}
QPushButton:default:hover {{
    background-color: {ACCENT_HOVER};
}}
QPushButton:default:pressed {{
    background-color: #0055b3;
}}

QComboBox {{
    background-color: white;
    border: 1px solid #d8d8dc;
    border-radius: 8px;
    padding: 4px 10px;
    min-height: 22px;
    color: #1c1c1e;
}}
QComboBox:hover {{
    border-color: #c0c0c4;
}}
QComboBox::drop-down {{
    border: none;
    width: 22px;
}}
QComboBox QAbstractItemView {{
    background-color: white;
    border: 1px solid #d8d8dc;
    border-radius: 8px;
    padding: 4px;
    selection-background-color: {ACCENT};
    selection-color: white;
    outline: none;
}}

QRadioButton {{
    spacing: 6px;
    padding: 4px 0;
    color: #1c1c1e;
}}

QListView, QListWidget {{
    background-color: white;
    border: 1px solid #e3e3e7;
    border-radius: 10px;
    padding: 6px;
    outline: none;
}}
QListView::item, QListWidget::item {{
    padding: 7px 10px;
    border-radius: 6px;
    color: #1c1c1e;
}}
QListView::item:hover, QListWidget::item:hover {{
    background-color: #f3f3f5;
}}
QListView::item:selected, QListWidget::item:selected {{
    background-color: {ACCENT};
    color: white;
}}

QSplitter::handle {{
    background-color: transparent;
    width: 8px;
}}

QLabel#preview {{
    background-color: #f8f8fa;
    border: 1px solid #e3e3e7;
    border-radius: 12px;
    color: #8a8a8e;
}}

QLabel#hint, QLabel#statusLabel {{
    color: #6c6c70;
}}

QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    background: transparent;
    color: transparent;
    border: none;
    max-width: 0px;
    max-height: 0px;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: rgba(0, 0, 0, 0.25);
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: rgba(0, 0, 0, 0.4);
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0; background: none;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background: rgba(0, 0, 0, 0.25);
    border-radius: 4px;
    min-width: 24px;
}}
"""

_DARK = f"""
QWidget {{
    color: #f5f5f7;
    font-size: 13px;
}}

QMainWindow, QWidget#central, QStackedWidget, QStackedWidget > QWidget {{
    background-color: #1e1e20;
}}

QWidget#sidebar {{
    background-color: #252528;
    border: none;
}}

QLabel#sidebarTitle {{
    color: #f5f5f7;
    font-size: 15px;
    font-weight: 600;
    padding: 4px 8px 8px 8px;
}}

QLabel#cacheLabel {{
    color: #98989d;
    font-size: 11px;
    padding: 0 6px;
}}

QListWidget#featureList {{
    background: transparent;
    border: none;
    outline: none;
    padding: 0;
}}
QListWidget#featureList::item {{
    padding: 9px 12px;
    margin: 2px 0;
    border-radius: 9px;
    color: #f5f5f7;
}}
QListWidget#featureList::item:hover {{
    background-color: rgba(255, 255, 255, 0.07);
}}
QListWidget#featureList::item:selected {{
    background-color: {ACCENT};
    color: white;
}}

QPushButton {{
    background-color: #3a3a3d;
    border: 1px solid #4a4a4d;
    border-radius: 8px;
    padding: 6px 14px;
    color: #f5f5f7;
    min-height: 20px;
}}
QPushButton:hover {{
    background-color: #45454a;
}}
QPushButton:pressed {{
    background-color: #2f2f33;
}}
QPushButton:default {{
    background-color: {ACCENT};
    color: white;
    border: 1px solid transparent;
}}
QPushButton:default:hover {{
    background-color: {ACCENT_HOVER};
}}

QComboBox {{
    background-color: #3a3a3d;
    border: 1px solid #4a4a4d;
    border-radius: 8px;
    padding: 4px 10px;
    min-height: 22px;
    color: #f5f5f7;
}}
QComboBox::drop-down {{
    border: none;
    width: 22px;
}}
QComboBox QAbstractItemView {{
    background-color: #2a2a2d;
    border: 1px solid #4a4a4d;
    border-radius: 8px;
    padding: 4px;
    selection-background-color: {ACCENT};
    selection-color: white;
    color: #f5f5f7;
    outline: none;
}}

QRadioButton {{
    spacing: 6px;
    padding: 4px 0;
    color: #f5f5f7;
}}

QListView, QListWidget {{
    background-color: #2a2a2d;
    border: 1px solid #38383b;
    border-radius: 10px;
    padding: 6px;
    outline: none;
    color: #f5f5f7;
}}
QListView::item, QListWidget::item {{
    padding: 7px 10px;
    border-radius: 6px;
    color: #f5f5f7;
}}
QListView::item:hover, QListWidget::item:hover {{
    background-color: #34343a;
}}
QListView::item:selected, QListWidget::item:selected {{
    background-color: {ACCENT};
    color: white;
}}

QSplitter::handle {{
    background-color: transparent;
    width: 8px;
}}

QLabel#preview {{
    background-color: #15151a;
    border: 1px solid #38383b;
    border-radius: 12px;
    color: #98989d;
}}

QLabel#hint, QLabel#statusLabel {{
    color: #98989d;
}}

QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    background: transparent;
    color: transparent;
    border: none;
    max-width: 0px;
    max-height: 0px;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: rgba(255, 255, 255, 0.25);
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: rgba(255, 255, 255, 0.4);
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0; background: none;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background: rgba(255, 255, 255, 0.25);
    border-radius: 4px;
    min-width: 24px;
}}
"""


def is_dark_mode(app: QApplication) -> bool:
    try:
        return app.styleHints().colorScheme() == Qt.ColorScheme.Dark
    except (AttributeError, Exception):
        # Fall back to palette luminance.
        bg = app.palette().color(QPalette.Window)
        return bg.lightnessF() < 0.5


def apply_app_style(app: QApplication) -> None:
    app.setStyleSheet(_DARK if is_dark_mode(app) else _LIGHT)
