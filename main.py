import os
import sys
import json
import shutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QTabWidget,
    QFileDialog, QMessageBox, QFontDialog, QTreeView,
    QDockWidget, QInputDialog, QMenu, QToolBar,
    QLabel, QStatusBar, QWidget, QSizePolicy,
    QFontComboBox, QSpinBox, QVBoxLayout, QHBoxLayout,
    QFrame, QToolButton, QDialog, QCheckBox, QComboBox,
    QGroupBox, QDialogButtonBox, QGridLayout,
)
from PyQt6.QtGui import (
    QAction, QKeySequence, QFont, QTextCharFormat, QFileSystemModel,
    QPainter, QColor, QPixmap, QIcon, QPaintEvent, QResizeEvent, QCloseEvent,
)
from PyQt6.QtCore import Qt, QSize, QRect, QSettings, QTimer, QByteArray

COL_NAME, COL_SIZE, COL_TYPE, COL_DATE = 0, 1, 2, 3
COLUMN_LABELS = {
    COL_NAME: "Name",
    COL_SIZE: "Size",
    COL_TYPE: "Type",
    COL_DATE: "Date Modified",
}
OPEN_FILTER = (
    "All Files (*.*);;Text Files (*.txt);;Python Files (*.py);;"
    "Markdown (*.md);;HTML Files (*.html *.htm)"
)
SAVE_FILTER = (
    "All Files (*.*);;Text Files (*.txt);;Markdown (*.md);;HTML Files (*.html *.htm)"
)

# ─────────────────────────────────────────────────────────────────────────────
# Stylesheets — Dark Theme
# ─────────────────────────────────────────────────────────────────────────────
DARK_THEME_QSS = """
/* ═══ DARK THEME ═══════════════════════════════════════════════════ */

* {
    font-family: "SF Pro Text", "Inter", "Helvetica Neue", "Segoe UI",
                 "Ubuntu", system-ui, sans-serif;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.90);
}

QMainWindow, QDialog { background-color: #0B0B14; }

/* ── Menu Bar ──────────────────────────────────────────────────────────── */
QMenuBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1C1C2E, stop:1 #12121C);
    border-bottom: 1px solid rgba(0, 0, 0, 0.55);
    padding: 2px 6px;
    spacing: 2px;
}
QMenuBar::item {
    padding: 4px 12px;
    border-radius: 6px;
    background: transparent;
    color: rgba(255, 255, 255, 0.78);
}
QMenuBar::item:selected {
    background: rgba(255, 255, 255, 0.09);
    color: rgba(255, 255, 255, 0.95);
}
QMenuBar::item:pressed {
    background: rgba(10, 132, 255, 0.20);
    color: #4DB8FF;
}

/* ── Drop-down Menus ───────────────────────────────────────────────────── */
QMenu {
    background-color: #1E1E30;
    border: 1px solid rgba(255, 255, 255, 0.11);
    padding: 5px 0;
    color: rgba(255, 255, 255, 0.88);
}
QMenu::item { padding: 6px 24px 6px 16px; }
QMenu::item:selected { background: #0A84FF; color: #FFFFFF; }
QMenu::item:disabled { color: rgba(255, 255, 255, 0.26); }
QMenu::separator { height: 1px; background: rgba(255,255,255,0.07); margin: 4px 0; }

/* ── Toolbar ───────────────────────────────────────────────────────────── */
QToolBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1A1A2C, stop:1 #0F0F1A);
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    border-bottom: 1px solid rgba(0, 0, 0, 0.55);
    spacing: 2px;
    padding: 4px 10px;
}
QToolBar::separator {
    width: 1px;
    background: rgba(255, 255, 255, 0.07);
    margin: 4px 8px;
}
QToolButton {
    border: none;
    border-radius: 7px;
    padding: 5px 12px;
    background: transparent;
    font-size: 12px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.78);
    min-width: 34px;
}
QToolButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255,255,255,0.12), stop:1 rgba(255,255,255,0.06));
    border: 1px solid rgba(255, 255, 255, 0.11);
    color: rgba(255, 255, 255, 0.96);
}
QToolButton:pressed {
    background: rgba(10, 132, 255, 0.20);
    border: 1px solid rgba(10, 132, 255, 0.38);
    color: #4DB8FF;
}
QToolButton:checked {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(10,132,255,0.28), stop:1 rgba(10,132,255,0.15));
    border: 1px solid rgba(10, 132, 255, 0.52);
    color: #4DB8FF;
}

/* ── Tab Bar ───────────────────────────────────────────────────────────── */
QTabWidget::pane { border: none; background: #0D0D18; }
QTabBar { background: #0F0F1A; }
QTabBar::tab {
    background: transparent;
    color: rgba(255, 255, 255, 0.38);
    border: none;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    padding: 8px 20px 8px 16px;
    font-size: 12px;
    min-width: 120px;
    max-width: 210px;
}
QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #16162A, stop:1 #0D0D18);
    color: rgba(255, 255, 255, 0.93);
    font-weight: 500;
    border-top: 2px solid #0A84FF;
}
QTabBar::tab:hover:!selected {
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.62);
}
QTabBar::close-button { subcontrol-position: right; padding: 2px; }

/* ── Text Editor ───────────────────────────────────────────────────────── */
QTextEdit {
    background-color: #0D0D18;
    color: rgba(255, 255, 255, 0.90);
    border: none;
    selection-background-color: rgba(10, 132, 255, 0.34);
    selection-color: #FFFFFF;
    font-size: 14px;
    padding: 4px 8px;
}

/* ── Dock Widgets ──────────────────────────────────────────────────────── */
QDockWidget { color: rgba(255,255,255,0.40); font-size: 11px; font-weight: 600; }
QDockWidget::title {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1C1C2E, stop:1 #14141F);
    padding: 7px 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom: 1px solid rgba(0, 0, 0, 0.45);
    text-align: left;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.38);
}
QDockWidget::close-button, QDockWidget::float-button {
    border: none; background: transparent; padding: 2px;
}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background: rgba(255, 255, 255, 0.09);
}

/* ── File Tree ─────────────────────────────────────────────────────────── */
QTreeView {
    background: #0F0F1C;
    alternate-background-color: #111120;
    border: none;
    outline: none;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.76);
    show-decoration-selected: 1;
}
QTreeView::item { padding: 4px; min-height: 24px; }
QTreeView::item:selected { background: #0A84FF; color: white; }
QTreeView::item:hover:!selected { background: rgba(255, 255, 255, 0.04); }
QHeaderView { background: #1A1A2C; }
QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1C1C2E, stop:1 #141420);
    color: rgba(255, 255, 255, 0.32);
    border: none;
    border-bottom: 1px solid rgba(0, 0, 0, 0.45);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    padding: 5px 10px;
    font-size: 11px;
    font-weight: 600;
}
QHeaderView::section:last { border-right: none; }
QHeaderView::section:hover { background: rgba(255, 255, 255, 0.06); }

/* ── Scrollbars ────────────────────────────────────────────────────────── */
QScrollBar:vertical { background: transparent; width: 8px; margin: 0; }
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.14);
    border-radius: 4px;
    min-height: 24px;
    margin: 0 1px;
}
QScrollBar::handle:vertical:hover { background: rgba(255, 255, 255, 0.30); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; height: 0; }
QScrollBar:horizontal { background: transparent; height: 8px; margin: 0; }
QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 0.14);
    border-radius: 4px;
    min-width: 24px;
    margin: 1px 0;
}
QScrollBar::handle:horizontal:hover { background: rgba(255, 255, 255, 0.30); }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; width: 0; }
QScrollBar::corner { background: transparent; }

/* ── Status Bar ────────────────────────────────────────────────────────── */
QStatusBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #13131E, stop:1 #0F0F18);
    border-top: 1px solid rgba(0, 0, 0, 0.55);
    color: rgba(255, 255, 255, 0.45);
    font-size: 11px;
    padding: 0 6px;
    min-height: 24px;
}
QStatusBar::item { border: none; }
QStatusBar QLabel {
    color: rgba(255, 255, 255, 0.45);
    font-size: 11px;
    padding: 0 8px;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

/* ── Format Sidebar Panel ──────────────────────────────────────────────── */
QWidget#formatPanel {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0F0F1C, stop:1 #12121E);
}
QLabel#panelSection {
    color: rgba(255, 255, 255, 0.28);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}
QLabel#panelFieldLabel { color: rgba(255, 255, 255, 0.36); font-size: 12px; }
QFrame#panelDivider {
    background: rgba(255, 255, 255, 0.06);
    border: none;
    max-height: 1px;
    color: rgba(255, 255, 255, 0.06);
}
QToolButton#formatBtn {
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 8px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255,255,255,0.07), stop:1 rgba(255,255,255,0.03));
    color: rgba(255, 255, 255, 0.84);
    padding: 0;
    min-width: 0;
}
QToolButton#formatBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255,255,255,0.14), stop:1 rgba(255,255,255,0.07));
    border-color: rgba(255, 255, 255, 0.20);
}
QToolButton#formatBtn:checked {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(10,132,255,0.30), stop:1 rgba(10,132,255,0.17));
    border-color: rgba(10, 132, 255, 0.58);
    color: #4DB8FF;
}
QToolButton#panelLink {
    border: none;
    background: transparent;
    color: #0A84FF;
    font-size: 12px;
    padding: 2px 0;
    text-align: left;
    min-width: 0;
}
QToolButton#panelLink:hover { color: #4DB8FF; }

/* ── Inputs ────────────────────────────────────────────────────────────── */
QFontComboBox, QComboBox {
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 7px;
    padding: 5px 8px;
    background: rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.85);
    font-size: 12px;
    min-height: 28px;
}
QFontComboBox:focus, QComboBox:focus {
    border-color: rgba(10, 132, 255, 0.65);
    background: rgba(10, 132, 255, 0.07);
}
QFontComboBox::drop-down, QComboBox::drop-down { border: none; width: 20px; }
QFontComboBox QAbstractItemView, QComboBox QAbstractItemView {
    background: #1E1E30;
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: rgba(255, 255, 255, 0.88);
    selection-background-color: #0A84FF;
    selection-color: white;
}
QSpinBox {
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 7px;
    padding: 5px 8px;
    background: rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.85);
    font-size: 12px;
    min-height: 28px;
}
QSpinBox:focus {
    border-color: rgba(10, 132, 255, 0.65);
    background: rgba(10, 132, 255, 0.07);
}
QSpinBox::up-button, QSpinBox::down-button { border: none; background: transparent; width: 18px; }
QLineEdit {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 7px;
    padding: 6px 10px;
    color: rgba(255, 255, 255, 0.90);
    font-size: 13px;
    selection-background-color: rgba(10, 132, 255, 0.32);
}
QLineEdit:focus { border-color: rgba(10, 132, 255, 0.65); }
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1B94FF, stop:1 #0A84FF);
    color: white;
    border: 1px solid rgba(10, 132, 255, 0.52);
    border-radius: 7px;
    padding: 7px 18px;
    font-size: 13px;
    font-weight: 500;
    min-width: 72px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2BA0FF, stop:1 #1A94FF);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0070DF, stop:1 #005CCF);
}
QPushButton:default { border-color: rgba(10, 132, 255, 0.80); }
QMessageBox { background: #1E1E30; }
QMessageBox QLabel { color: rgba(255, 255, 255, 0.90); }

/* ── Dialog / Settings ────────────────────────────────────────────────────── */
QDialog { background: #1E1E30; }
QGroupBox {
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 8px;
    margin-top: 14px;
    padding: 16px 12px 12px 12px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.72);
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: rgba(255, 255, 255, 0.52);
}
QCheckBox {
    spacing: 8px;
    color: rgba(255, 255, 255, 0.85);
    font-size: 12px;
}
QCheckBox::indicator {
    width: 16px; height: 16px;
    border: 1px solid rgba(255, 255, 255, 0.20);
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.06);
}
QCheckBox::indicator:checked {
    background: #0A84FF;
    border-color: #0A84FF;
}
QCheckBox::indicator:hover {
    border-color: rgba(255, 255, 255, 0.35);
}
"""

# ─────────────────────────────────────────────────────────────────────────────
# Stylesheets — Light Theme
# ─────────────────────────────────────────────────────────────────────────────
LIGHT_THEME_QSS = """
/* ═══ LIGHT THEME ══════════════════════════════════════════════════ */

* {
    font-family: "SF Pro Text", "Inter", "Helvetica Neue", "Segoe UI",
                 "Ubuntu", system-ui, sans-serif;
    font-size: 13px;
    color: #1C1C1E;
}

QMainWindow, QDialog { background-color: #F2F2F7; }

/* ── Menu Bar ──────────────────────────────────────────────────────────── */
QMenuBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFFFFF, stop:1 #F5F5FA);
    border-bottom: 1px solid rgba(0, 0, 0, 0.10);
    padding: 2px 6px;
    spacing: 2px;
    color: #1C1C1E;
}
QMenuBar::item {
    padding: 4px 12px;
    border-radius: 6px;
    background: transparent;
    color: #1C1C1E;
}
QMenuBar::item:selected { background: rgba(0, 0, 0, 0.07); }
QMenuBar::item:pressed {
    background: rgba(0, 122, 255, 0.12);
    color: #007AFF;
}

/* ── Drop-down Menus ───────────────────────────────────────────────────── */
QMenu {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.13);
    padding: 5px 0;
    color: #1C1C1E;
}
QMenu::item { padding: 6px 24px 6px 16px; }
QMenu::item:selected { background: #007AFF; color: white; }
QMenu::item:disabled { color: #AEAEB2; }
QMenu::separator { height: 1px; background: rgba(0, 0, 0, 0.08); margin: 4px 0; }

/* ── Toolbar ───────────────────────────────────────────────────────────── */
QToolBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFFFFF, stop:1 #F4F4F9);
    border-bottom: 1px solid rgba(0, 0, 0, 0.10);
    spacing: 2px;
    padding: 4px 10px;
}
QToolBar::separator { width: 1px; background: rgba(0,0,0,0.09); margin: 4px 8px; }
QToolButton {
    border: none;
    border-radius: 7px;
    padding: 5px 12px;
    background: transparent;
    font-size: 12px;
    font-weight: 500;
    color: #1C1C1E;
    min-width: 34px;
}
QToolButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0,0,0,0.07), stop:1 rgba(0,0,0,0.04));
    border: 1px solid rgba(0, 0, 0, 0.09);
}
QToolButton:pressed {
    background: rgba(0, 122, 255, 0.12);
    border: 1px solid rgba(0, 122, 255, 0.28);
    color: #007AFF;
}
QToolButton:checked {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0,122,255,0.15), stop:1 rgba(0,122,255,0.09));
    border: 1px solid rgba(0, 122, 255, 0.35);
    color: #007AFF;
}

/* ── Tab Bar ───────────────────────────────────────────────────────────── */
QTabWidget::pane { border: none; background: #FFFFFF; }
QTabBar { background: #EBEBF0; }
QTabBar::tab {
    background: #EBEBF0;
    color: #8E8E93;
    border: none;
    border-right: 1px solid rgba(0,0,0,0.08);
    padding: 8px 20px 8px 16px;
    font-size: 12px;
    min-width: 120px;
    max-width: 210px;
}
QTabBar::tab:selected {
    background: #FFFFFF;
    color: #1C1C1E;
    font-weight: 500;
    border-top: 2px solid #007AFF;
}
QTabBar::tab:hover:!selected { background: #E2E2E8; color: #3C3C3E; }
QTabBar::close-button { subcontrol-position: right; padding: 2px; }

/* ── Text Editor ───────────────────────────────────────────────────────── */
QTextEdit {
    background: #FFFFFF;
    color: #1C1C1E;
    border: none;
    selection-background-color: rgba(0, 122, 255, 0.18);
    selection-color: #1C1C1E;
    font-size: 14px;
    padding: 4px 8px;
}

/* ── Dock Widgets ──────────────────────────────────────────────────────── */
QDockWidget { color: #8E8E93; font-size: 11px; font-weight: 600; }
QDockWidget::title {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FEFEFE, stop:1 #F4F4F9);
    padding: 7px 12px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.10);
    text-align: left;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: #8E8E93;
}
QDockWidget::close-button, QDockWidget::float-button {
    border: none; background: transparent; padding: 2px;
}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background: rgba(0, 0, 0, 0.07);
}

/* ── File Tree ─────────────────────────────────────────────────────────── */
QTreeView {
    background: #F5F5F7;
    alternate-background-color: #F0F0F5;
    border: none;
    outline: none;
    font-size: 12px;
    color: #1C1C1E;
    show-decoration-selected: 1;
}
QTreeView::item { padding: 4px; min-height: 24px; }
QTreeView::item:selected { background: #007AFF; color: white; }
QTreeView::item:hover:!selected { background: rgba(0, 0, 0, 0.04); }
QHeaderView { background: #F0F0F5; }
QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FAFAFA, stop:1 #F0F0F5);
    color: #8E8E93;
    border: none;
    border-bottom: 1px solid rgba(0, 0, 0, 0.10);
    border-right: 1px solid rgba(0, 0, 0, 0.07);
    padding: 5px 10px;
    font-size: 11px;
    font-weight: 600;
}
QHeaderView::section:last { border-right: none; }
QHeaderView::section:hover { background: #E8E8ED; }

/* ── Scrollbars ────────────────────────────────────────────────────────── */
QScrollBar:vertical { background: transparent; width: 8px; margin: 0; }
QScrollBar::handle:vertical {
    background: rgba(0,0,0,0.18);
    border-radius: 4px;
    min-height: 24px;
    margin: 0 1px;
}
QScrollBar::handle:vertical:hover { background: rgba(0,0,0,0.32); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; height: 0; }
QScrollBar:horizontal { background: transparent; height: 8px; margin: 0; }
QScrollBar::handle:horizontal {
    background: rgba(0,0,0,0.18);
    border-radius: 4px;
    min-width: 24px;
    margin: 1px 0;
}
QScrollBar::handle:horizontal:hover { background: rgba(0,0,0,0.32); }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; width: 0; }
QScrollBar::corner { background: transparent; }

/* ── Status Bar ────────────────────────────────────────────────────────── */
QStatusBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FAFAFA, stop:1 #F4F4F9);
    border-top: 1px solid rgba(0, 0, 0, 0.10);
    color: #8E8E93;
    font-size: 11px;
    padding: 0 6px;
    min-height: 24px;
}
QStatusBar::item { border: none; }
QStatusBar QLabel {
    color: #8E8E93;
    font-size: 11px;
    padding: 0 8px;
    border-right: 1px solid rgba(0, 0, 0, 0.08);
}

/* ── Format Sidebar Panel ──────────────────────────────────────────────── */
QWidget#formatPanel { background: #F5F5FA; }
QLabel#panelSection {
    color: #8E8E93;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}
QLabel#panelFieldLabel { color: #8E8E93; font-size: 12px; }
QFrame#panelDivider {
    background: rgba(0, 0, 0, 0.09);
    border: none;
    max-height: 1px;
    color: rgba(0, 0, 0, 0.09);
}
QToolButton#formatBtn {
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 8px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFFFFF, stop:1 #F4F4F9);
    color: #1C1C1E;
    padding: 0;
    min-width: 0;
}
QToolButton#formatBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #F6F6FF, stop:1 #EBEBF5);
    border-color: rgba(0, 0, 0, 0.18);
}
QToolButton#formatBtn:checked {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0,122,255,0.15), stop:1 rgba(0,122,255,0.09));
    border-color: rgba(0, 122, 255, 0.40);
    color: #007AFF;
}
QToolButton#panelLink {
    border: none;
    background: transparent;
    color: #007AFF;
    font-size: 12px;
    padding: 2px 0;
    text-align: left;
    min-width: 0;
}
QToolButton#panelLink:hover { color: #005CC8; }

/* ── Inputs ────────────────────────────────────────────────────────────── */
QFontComboBox, QComboBox {
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 7px;
    padding: 5px 8px;
    background: #FFFFFF;
    color: #1C1C1E;
    font-size: 12px;
    min-height: 28px;
}
QFontComboBox:focus, QComboBox:focus { border-color: #007AFF; }
QFontComboBox::drop-down, QComboBox::drop-down { border: none; width: 20px; }
QFontComboBox QAbstractItemView, QComboBox QAbstractItemView {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.12);
    color: #1C1C1E;
    selection-background-color: #007AFF;
    selection-color: white;
}
QSpinBox {
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 7px;
    padding: 5px 8px;
    background: #FFFFFF;
    color: #1C1C1E;
    font-size: 12px;
    min-height: 28px;
}
QSpinBox:focus { border-color: #007AFF; }
QSpinBox::up-button, QSpinBox::down-button { border: none; background: transparent; width: 18px; }
QLineEdit {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 7px;
    padding: 6px 10px;
    color: #1C1C1E;
    font-size: 13px;
}
QLineEdit:focus { border-color: #007AFF; }
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2B8BFF, stop:1 #007AFF);
    color: white;
    border: 1px solid rgba(0, 122, 255, 0.42);
    border-radius: 7px;
    padding: 7px 18px;
    font-size: 13px;
    font-weight: 500;
    min-width: 72px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3D99FF, stop:1 #1A8AFF);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0066DD, stop:1 #0055CC);
}
QPushButton:default { border-color: rgba(0, 122, 255, 0.72); }
QMessageBox { background: #FFFFFF; }
QMessageBox QLabel { color: #1C1C1E; }

/* ── Dialog / Settings ────────────────────────────────────────────────────── */
QDialog { background: #F2F2F7; }
QGroupBox {
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 8px;
    margin-top: 14px;
    padding: 16px 12px 12px 12px;
    font-weight: 600;
    color: #3C3C3E;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: #8E8E93;
}
QCheckBox {
    spacing: 8px;
    color: #1C1C1E;
    font-size: 12px;
}
QCheckBox::indicator {
    width: 16px; height: 16px;
    border: 1px solid rgba(0, 0, 0, 0.18);
    border-radius: 4px;
    background: #FFFFFF;
}
QCheckBox::indicator:checked {
    background: #007AFF;
    border-color: #007AFF;
}
QCheckBox::indicator:hover {
    border-color: rgba(0, 0, 0, 0.30);
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# Settings defaults
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_SETTINGS = {
    "theme_mode": "dark",
    "restore_layout": True,
    "restore_explorer_state": True,
    "restore_sidebar_state": True,
}


# ─────────────────────────────────────────────────────────────────────────────
# Settings Dialog
# ─────────────────────────────────────────────────────────────────────────────

class SettingsDialog(QDialog):

    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(480, 380)
        self._settings = dict(current_settings or DEFAULT_SETTINGS)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(16)

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 18px; font-weight: 700; padding-bottom: 4px;")
        layout.addWidget(title)

        self._tab_widget = QTabWidget()
        layout.addWidget(self._tab_widget)

        self._build_appearance_tab()
        self._build_layout_tab()

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.RestoreDefaults
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        _restore_btn = btn_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        if _restore_btn is not None:
            _restore_btn.clicked.connect(self._restore_defaults)
        layout.addWidget(btn_box)

    def _build_appearance_tab(self):
        page = QWidget()
        vbox = QVBoxLayout(page)
        vbox.setContentsMargins(12, 16, 12, 12)
        vbox.setSpacing(12)

        grp = QGroupBox("Theme")
        grid = QGridLayout(grp)
        grid.setContentsMargins(12, 16, 12, 12)
        grid.setVerticalSpacing(10)

        grid.addWidget(QLabel("Color theme:"), 0, 0)
        self._theme_combo = QComboBox()
        self._theme_combo.addItems(["Dark", "Light", "Auto (follow system)"])
        mode = self._settings.get("theme_mode", "dark")
        idx_map = {"dark": 0, "light": 1, "auto": 2}
        self._theme_combo.setCurrentIndex(idx_map.get(mode, 0))
        grid.addWidget(self._theme_combo, 0, 1)

        vbox.addWidget(grp)
        vbox.addStretch()

        self._tab_widget.addTab(page, "Appearance")

    def _build_layout_tab(self):
        page = QWidget()
        vbox = QVBoxLayout(page)
        vbox.setContentsMargins(12, 16, 12, 12)
        vbox.setSpacing(12)

        grp = QGroupBox("Persistence")
        gvbox = QVBoxLayout(grp)
        gvbox.setContentsMargins(12, 16, 12, 12)
        gvbox.setSpacing(10)

        self._restore_layout_cb = QCheckBox(
            "Remember window size, position, and dock layout on restart")
        self._restore_layout_cb.setChecked(
            self._settings.get("restore_layout", True))
        gvbox.addWidget(self._restore_layout_cb)

        self._restore_explorer_cb = QCheckBox(
            "Remember Explorer dock visibility and position")
        self._restore_explorer_cb.setChecked(
            self._settings.get("restore_explorer_state", True))
        gvbox.addWidget(self._restore_explorer_cb)

        self._restore_sidebar_cb = QCheckBox(
            "Remember Format Sidebar visibility and position")
        self._restore_sidebar_cb.setChecked(
            self._settings.get("restore_sidebar_state", True))
        gvbox.addWidget(self._restore_sidebar_cb)

        vbox.addWidget(grp)
        vbox.addStretch()

        self._tab_widget.addTab(page, "Layout")


    def get_settings(self) -> dict:
        mode_map = {0: "dark", 1: "light", 2: "auto"}
        return {
            "theme_mode": mode_map.get(self._theme_combo.currentIndex(), "dark"),
            "restore_layout": self._restore_layout_cb.isChecked(),
            "restore_explorer_state": self._restore_explorer_cb.isChecked(),
            "restore_sidebar_state": self._restore_sidebar_cb.isChecked(),
        }

    def _restore_defaults(self):
        self._settings = dict(DEFAULT_SETTINGS)
        self._theme_combo.setCurrentIndex(0)
        self._restore_layout_cb.setChecked(True)
        self._restore_explorer_cb.setChecked(True)
        self._restore_sidebar_cb.setChecked(True)


# ─────────────────────────────────────────────────────────────────────────────
# Line-number gutter
# ─────────────────────────────────────────────────────────────────────────────

class LineNumberArea(QWidget):

    def __init__(self, editor: "CodeEditor"):
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self._editor.gutter_width(), 0)

    def paintEvent(self, a0: QPaintEvent | None) -> None:  # type: ignore[override]
        self._editor.paint_line_numbers(a0)


class CodeEditor(QTextEdit):

    _GUTTER_RIGHT_PAD = 8
    _GUTTER_LEFT_PAD  = 10
    _DOC_MARGIN       = 16

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lna         = LineNumberArea(self)
        self._gutter_dark = True
        self.file_path: str | None = None

        doc = self.document()
        if doc is not None:
            doc.setDocumentMargin(self._DOC_MARGIN)
            doc.blockCountChanged.connect(self._refresh_gutter_width)
            doc.contentsChanged.connect(self._lna.update)

        vsb = self.verticalScrollBar()
        if vsb is not None:
            vsb.valueChanged.connect(self._lna.update)

        self.cursorPositionChanged.connect(self._lna.update)
        self._refresh_gutter_width()

    def gutter_width(self) -> int:
        doc = self.document()
        block_count = doc.blockCount() if doc is not None else 1
        digits = max(3, len(str(max(1, block_count))))
        return self._GUTTER_LEFT_PAD + digits * self.fontMetrics().horizontalAdvance("0") + self._GUTTER_RIGHT_PAD

    def _refresh_gutter_width(self):
        self.setViewportMargins(self.gutter_width(), 0, 0, 0)
        self._lna.update()

    def setFont(self, a0: QFont) -> None:  # type: ignore[override]
        super().setFont(a0)
        self._refresh_gutter_width()

    def resizeEvent(self, a0: QResizeEvent | None) -> None:  # type: ignore[override]
        super().resizeEvent(a0)  # type: ignore[arg-type]
        cr = self.contentsRect()
        self._lna.setGeometry(QRect(cr.left(), cr.top(), self.gutter_width(), cr.height()))

    def paint_line_numbers(self, event):
        painter = QPainter(self._lna)
        dark = self._gutter_dark

        if dark:
            c_bg         = QColor(13, 13, 24)
            c_sep        = QColor(255, 255, 255, 18)
            c_num        = QColor(255, 255, 255, 72)
            c_active_bg  = QColor(255, 255, 255, 10)
            c_active_num = QColor(255, 255, 255, 220)
        else:
            c_bg         = QColor(240, 240, 245)
            c_sep        = QColor(220, 220, 226)
            c_num        = QColor(174, 174, 178)
            c_active_bg  = QColor(232, 232, 238)
            c_active_num = QColor(29, 29, 31)

        painter.fillRect(event.rect(), c_bg)

        sep_x = self._lna.width() - 1
        painter.setPen(c_sep)
        painter.drawLine(sep_x, event.rect().top(), sep_x, event.rect().bottom())

        ln_font = QFont(self.font())
        ln_font.setPointSize(max(9, self.font().pointSize() - 1))
        painter.setFont(ln_font)

        doc = self.document()
        vsb = self.verticalScrollBar()
        if doc is None or vsb is None:
            painter.end()
            return

        doc_layout  = doc.documentLayout()
        if doc_layout is None:
            painter.end()
            return
        scroll_y    = vsb.value()
        lna_height  = self._lna.height()
        current_blk = self.textCursor().block()
        text_rect_w = self._lna.width() - self._GUTTER_RIGHT_PAD

        block = doc.begin()
        num   = 0

        while block.isValid():
            num += 1
            br = doc_layout.blockBoundingRect(block)
            y  = int(br.top()) - scroll_y
            h  = int(br.height())

            if y > lna_height:
                break

            if y + h >= 0:
                if block == current_blk:
                    painter.fillRect(0, y, sep_x, h, c_active_bg)
                    painter.setPen(c_active_num)
                else:
                    painter.setPen(c_num)

                painter.drawText(
                    0, y, text_rect_w, h,
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                    str(num),
                )

            block = block.next()

        painter.end()


# ─────────────────────────────────────────────────────────────────────────────
# Main application window
# ─────────────────────────────────────────────────────────────────────────────

class PlainNotepad(QMainWindow):

    _THEME_CYCLE = {"dark": "light", "light": "auto", "auto": "dark"}
    _THEME_LABELS = {
        "dark":  "☾  Dark",
        "light": "☼  Light",
        "auto":  "⊙  Auto",
    }
    _THEME_TIPS = {
        "dark":  "Dark mode  —  click for Light",
        "light": "Light mode  —  click for Auto",
        "auto":  "Auto (follows system)  —  click for Dark",
    }

    def __init__(self):
        super().__init__()

        self.setWindowTitle("M-Pad")
        self.resize(1100, 680)

        self._qsettings = QSettings("M-Pad", "M-Pad")
        self._prefs = self._load_settings()
        self._theme_mode = self._prefs.get("theme_mode", "dark")
        self._last_system_dark = self._detect_system_dark()

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self.setCentralWidget(self.tab_widget)

        self._create_format_actions()
        self._build_explorer()
        self._build_format_panel()
        self._build_menu()
        self._build_toolbar()
        self._build_status_bar()

        self._apply_theme()
        self.new_file()

        self._restore_layout()

        try:
            _app = QApplication.instance()
            if isinstance(_app, QApplication):
                _hints = _app.styleHints()
                if _hints is not None:
                    _hints.colorSchemeChanged.connect(
                        self._on_system_scheme_changed)
        except AttributeError:
            pass

        self._auto_poll_timer = QTimer(self)
        self._auto_poll_timer.setInterval(2000)
        self._auto_poll_timer.timeout.connect(self._poll_system_theme)
        if self._theme_mode == "auto":
            self._auto_poll_timer.start()

        # Debounced word count — only recalculate 400 ms after last keystroke
        self._wc_timer = QTimer(self)
        self._wc_timer.setSingleShot(True)
        self._wc_timer.setInterval(400)
        self._wc_timer.timeout.connect(self._do_word_count_update)

        self._word_wrap: bool = True  # track word-wrap state

    # ══════════════════════════════════════════════════════════════════════════
    # Settings persistence
    # ══════════════════════════════════════════════════════════════════════════

    def _load_settings(self) -> dict:
        prefs = dict(DEFAULT_SETTINGS)
        raw = self._qsettings.value("user_prefs")
        if raw:
            try:
                loaded = json.loads(raw) if isinstance(raw, str) else raw
                prefs.update(loaded)
            except (json.JSONDecodeError, TypeError):
                pass
        return prefs

    def _save_settings(self):
        self._qsettings.setValue("user_prefs", json.dumps(self._prefs))
        self._qsettings.sync()

    def _save_layout(self):
        self._qsettings.setValue("window_geometry", self.saveGeometry())
        self._qsettings.setValue("window_state", self.saveState())
        self._qsettings.setValue("explorer_visible", self.file_dock.isVisible())
        self._qsettings.setValue("sidebar_visible", self.format_dock.isVisible())
        self._qsettings.sync()

    def _restore_layout(self):
        if not self._prefs.get("restore_layout", True):
            return

        geom = self._qsettings.value("window_geometry")
        if geom and isinstance(geom, QByteArray):
            self.restoreGeometry(geom)

        state = self._qsettings.value("window_state")
        if state and isinstance(state, QByteArray):
            self.restoreState(state)

        if self._prefs.get("restore_explorer_state", True):
            vis = self._qsettings.value("explorer_visible", False)
            self.file_dock.setVisible(
                (vis == "true" or vis is True) if isinstance(vis, (str, bool)) else False)
        else:
            self.file_dock.hide()

        if self._prefs.get("restore_sidebar_state", True):
            vis = self._qsettings.value("sidebar_visible", False)
            self.format_dock.setVisible(
                (vis == "true" or vis is True) if isinstance(vis, (str, bool)) else False)
        else:
            self.format_dock.hide()

    # ══════════════════════════════════════════════════════════════════════════
    # Settings dialog
    # ══════════════════════════════════════════════════════════════════════════

    def open_settings(self):
        dlg = SettingsDialog(self, current_settings=self._prefs)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            new_prefs = dlg.get_settings()
            old_theme = self._theme_mode
            self._prefs = new_prefs
            self._theme_mode = new_prefs["theme_mode"]
            self._save_settings()

            if self._theme_mode != old_theme:
                self._apply_theme()

            if self._theme_mode == "auto":
                self._auto_poll_timer.start()
            else:
                self._auto_poll_timer.stop()

    # ══════════════════════════════════════════════════════════════════════════
    # Theme management
    # ══════════════════════════════════════════════════════════════════════════

    @staticmethod
    def _detect_system_dark() -> bool:
        try:
            _app = QApplication.instance()
            if not isinstance(_app, QApplication):
                return True
            _hints = _app.styleHints()
            if _hints is None:
                return True
            cs = _hints.colorScheme()
            return cs == Qt.ColorScheme.Dark
        except AttributeError:
            return True

    def _apply_theme(self):
        mode = self._theme_mode
        dark = self._detect_system_dark() if mode == "auto" else (mode == "dark")

        _app = QApplication.instance()
        if isinstance(_app, QApplication):
            _app.setStyleSheet(DARK_THEME_QSS if dark else LIGHT_THEME_QSS)

        for i in range(self.tab_widget.count()):
            ed = self.tab_widget.widget(i)
            if isinstance(ed, CodeEditor):
                ed._gutter_dark = dark
                ed._lna.update()

        if hasattr(self, "_theme_act"):
            self._theme_act.setText(self._THEME_LABELS[mode])
            self._theme_act.setToolTip(self._THEME_TIPS[mode])

    def _cycle_theme(self, _checked=False):
        self._theme_mode = self._THEME_CYCLE[self._theme_mode]
        self._prefs["theme_mode"] = self._theme_mode
        self._save_settings()
        self._apply_theme()
        if self._theme_mode == "auto":
            self._auto_poll_timer.start()
        else:
            self._auto_poll_timer.stop()

    def _on_system_scheme_changed(self):
        if self._theme_mode == "auto":
            self._last_system_dark = self._detect_system_dark()
            self._apply_theme()

    def _poll_system_theme(self):
        if self._theme_mode != "auto":
            return
        current = self._detect_system_dark()
        if current != self._last_system_dark:
            self._last_system_dark = current
            self._apply_theme()

    # ══════════════════════════════════════════════════════════════════════════
    # Format actions
    # ══════════════════════════════════════════════════════════════════════════

    def _create_format_actions(self):
        self.bold_action = QAction("B", self)
        self.bold_action.setShortcut(QKeySequence.StandardKey.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.toggle_bold)
        self.addAction(self.bold_action)

        self.italic_action = QAction("I", self)
        self.italic_action.setShortcut(QKeySequence.StandardKey.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.triggered.connect(self.toggle_italic)
        self.addAction(self.italic_action)

        self.underline_action = QAction("U", self)
        self.underline_action.setShortcut(QKeySequence.StandardKey.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.triggered.connect(self.toggle_underline)
        self.addAction(self.underline_action)

    # ══════════════════════════════════════════════════════════════════════════
    # UI Construction
    # ══════════════════════════════════════════════════════════════════════════

    def _build_menu(self):
        mb = self.menuBar()
        assert mb is not None

        file_menu = mb.addMenu("File")
        assert file_menu is not None
        self._make_action(file_menu, "New",
                          QKeySequence.StandardKey.New, self.new_file)
        self._make_action(file_menu, "Open File\u2026",
                          QKeySequence.StandardKey.Open, self.open_file)
        self._make_action(file_menu, "Open Project Folder\u2026",
                          callback=self.open_folder)
        file_menu.addSeparator()
        self._make_action(file_menu, "Save",
                          QKeySequence.StandardKey.Save, self.save_file)
        self._make_action(file_menu, "Save As\u2026",
                          QKeySequence.StandardKey.SaveAs, self.save_file_as)
        file_menu.addSeparator()
        self._make_action(file_menu, "Exit",
                          QKeySequence.StandardKey.Quit, self.close)

        edit_menu = mb.addMenu("Edit")
        assert edit_menu is not None
        self._make_action(edit_menu, "Undo",
                          QKeySequence.StandardKey.Undo,  self._editor_undo)
        self._make_action(edit_menu, "Redo",
                          QKeySequence.StandardKey.Redo,  self._editor_redo)
        edit_menu.addSeparator()
        self._make_action(edit_menu, "Cut",
                          QKeySequence.StandardKey.Cut,   self._editor_cut)
        self._make_action(edit_menu, "Copy",
                          QKeySequence.StandardKey.Copy,  self._editor_copy)
        self._make_action(edit_menu, "Paste",
                          QKeySequence.StandardKey.Paste, self._editor_paste)
        edit_menu.addSeparator()
        self._make_action(edit_menu, "Settings\u2026",
                          QKeySequence("Ctrl+,"), self.open_settings)

        view_menu = mb.addMenu("View")
        assert view_menu is not None
        exp_toggle = self.file_dock.toggleViewAction()
        if exp_toggle is not None:
            exp_toggle.setText("Explorer")
            exp_toggle.setShortcut(QKeySequence("Ctrl+Shift+E"))
            view_menu.addAction(exp_toggle)

        sb_toggle = self.format_dock.toggleViewAction()
        if sb_toggle is not None:
            sb_toggle.setText("Format Sidebar")
            sb_toggle.setShortcut(QKeySequence("Ctrl+Shift+F"))
            view_menu.addAction(sb_toggle)

        view_menu.addSeparator()
        self._wrap_action = self._make_action(
            view_menu, "Word Wrap",
            QKeySequence("Ctrl+Shift+W"), self._toggle_word_wrap)
        self._wrap_action.setCheckable(True)
        self._wrap_action.setChecked(True)

        view_menu.addSeparator()
        self._make_action(view_menu, "Zoom In",
                          QKeySequence.StandardKey.ZoomIn, self._zoom_in)
        self._make_action(view_menu, "Zoom Out",
                          QKeySequence.StandardKey.ZoomOut, self._zoom_out)
        self._make_action(view_menu, "Reset Zoom",
                          QKeySequence("Ctrl+0"), self._zoom_reset)

        view_menu.addSeparator()
        self._make_action(view_menu, "Save Layout Now",
                          callback=self._manual_save_layout)

        help_menu = mb.addMenu("Help")
        assert help_menu is not None
        self._make_action(help_menu, "About M-Pad",
                          callback=self.show_about_dialog)

    def _build_toolbar(self):
        tb = QToolBar("Main Toolbar", self)
        tb.setObjectName("mainToolBar")
        tb.setMovable(False)
        tb.setFloatable(False)
        tb.setIconSize(QSize(16, 16))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, tb)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Preferred)
        tb.addWidget(spacer)
        tb.addSeparator()

        self._theme_act = self._make_tb_action(
            self._THEME_LABELS["dark"], self._cycle_theme,
            self._THEME_TIPS["dark"])
        tb.addAction(self._theme_act)
        tb.addSeparator()

        self._explorer_tb_action = self._make_tb_action(
            "\u2318  Explorer", self._toggle_explorer,
            "Toggle file explorer  (Ctrl+Shift+E)", checkable=True)
        self._explorer_tb_action.setChecked(False)
        tb.addAction(self._explorer_tb_action)

        self._sidebar_tb_action = self._make_tb_action(
            "\u2630  Sidebar", self._toggle_sidebar,
            "Toggle format sidebar  (Ctrl+Shift+S)", checkable=True)
        self._sidebar_tb_action.setChecked(False)
        tb.addAction(self._sidebar_tb_action)

        tb.addSeparator()

        self._wrap_tb_action = self._make_tb_action(
            "\u21a9  Wrap", self._toggle_word_wrap,
            "Toggle word wrap  (Ctrl+Shift+W)", checkable=True)
        self._wrap_tb_action.setChecked(True)
        tb.addAction(self._wrap_tb_action)

        tb.addSeparator()

        tb.addAction(self._make_tb_action("\u2212", self._zoom_out, "Zoom out  (Ctrl+-)"))
        tb.addAction(self._make_tb_action("+", self._zoom_in, "Zoom in  (Ctrl++)"))

    def _build_status_bar(self):
        sb = QStatusBar(self)
        self.setStatusBar(sb)

        # Left side: file info (non-permanent = left-aligned)
        self._status_file = QLabel("")
        sb.addWidget(self._status_file)

        # Right side: permanent labels with separator styling from QSS
        self._status_pos   = QLabel("Line 1,  Col 1")
        self._status_words = QLabel("Words: 0")
        self._status_chars = QLabel("Chars: 0")
        self._status_enc   = QLabel("UTF-8")
        for lbl in (self._status_pos, self._status_words,
                    self._status_chars, self._status_enc):
            sb.addPermanentWidget(lbl)

    def _build_explorer(self, root_path=None):
        root_path = root_path or os.path.expanduser("~")

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(root_path)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(root_path))
        self.tree_view.setAnimated(True)
        self.tree_view.setUniformRowHeights(True)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(COL_NAME, Qt.SortOrder.AscendingOrder)

        self.tree_view.setColumnHidden(COL_SIZE, True)
        self.tree_view.setColumnHidden(COL_DATE, True)
        self.tree_view.setColumnWidth(COL_NAME, 240)
        header = self.tree_view.header()
        assert header is not None
        header.setStretchLastSection(False)
        header.setSectionResizeMode(COL_NAME, header.ResizeMode.Stretch)

        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.on_tree_context_menu)
        self.tree_view.doubleClicked.connect(self.on_tree_double_clicked)
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.on_header_context_menu)

        self.file_dock = QDockWidget("Explorer", self)
        self.file_dock.setObjectName("explorerDock")
        self.file_dock.setWidget(self.tree_view)
        self.file_dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.file_dock.setMinimumWidth(200)
        self.file_dock.visibilityChanged.connect(self._sync_explorer_action)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.file_dock)
        self.file_dock.hide()

    def _build_format_panel(self):
        panel = QWidget()
        panel.setObjectName("formatPanel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(6)

        def section_lbl(text):
            lbl = QLabel(text)
            lbl.setObjectName("panelSection")
            return lbl

        def divider():
            line = QFrame()
            line.setObjectName("panelDivider")
            line.setFrameShape(QFrame.Shape.HLine)
            return line

        layout.addWidget(section_lbl("Font"))
        layout.addSpacing(4)

        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont("Consolas"))
        self.font_combo.currentFontChanged.connect(self._apply_font_family)
        layout.addWidget(self.font_combo)

        size_row = QHBoxLayout()
        size_row.setSpacing(8)
        size_lbl = QLabel("Size")
        size_lbl.setObjectName("panelFieldLabel")
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(6, 144)
        self.font_size_spin.setValue(13)
        self.font_size_spin.setSuffix(" pt")
        self.font_size_spin.setFixedWidth(90)
        self.font_size_spin.valueChanged.connect(self._apply_font_size)
        size_row.addWidget(size_lbl)
        size_row.addWidget(self.font_size_spin)
        size_row.addStretch()
        layout.addLayout(size_row)

        font_dlg_btn = QToolButton()
        font_dlg_btn.setText("Font options\u2026")
        font_dlg_btn.setObjectName("panelLink")
        font_dlg_btn.clicked.connect(self.choose_font)
        layout.addWidget(font_dlg_btn)

        layout.addSpacing(6)
        layout.addWidget(divider())
        layout.addSpacing(6)

        layout.addWidget(section_lbl("Font Style"))
        layout.addSpacing(6)

        style_row = QHBoxLayout()
        style_row.setSpacing(15)
        for action, extra in [
            (self.bold_action,      "font-weight:900; font-size:15px;"),
            (self.italic_action,    "font-style:italic; font-size:15px;"),
            (self.underline_action, "text-decoration:underline; font-size:15px;"),
        ]:
            btn = QToolButton()
            btn.setDefaultAction(action)
            btn.setFixedSize(42, 42)
            btn.setObjectName("formatBtn")
            btn.setStyleSheet(btn.styleSheet() + extra)
            style_row.addWidget(btn)
        style_row.addStretch()
        layout.addLayout(style_row)

        layout.addSpacing(6)
        layout.addWidget(divider())
        layout.addSpacing(6)

        layout.addWidget(section_lbl("Text Alignment"))
        layout.addSpacing(6)

        def _make_align_icon(widths, align_mode):
            sz = 32
            pm = QPixmap(sz, sz)
            pm.fill(QColor(80, 80, 80, 80))
            p = QPainter(pm)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            bar_h = 2
            gap = 6
            total_h = 3 * bar_h + 2 * gap
            y0 = (sz - total_h) // 2
            for i, w in enumerate(widths):
                y = y0 + i * (bar_h + gap)
                if align_mode == "left":
                    x = 3
                elif align_mode == "right":
                    x = sz - 3 - w
                elif align_mode == "center":
                    x = (sz - w) // 2
                else:
                    x = 3
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(QColor(255, 255, 255, 200))
                p.drawRoundedRect(x, y, w, bar_h, 1, 1)
            p.end()
            return QIcon(pm)

        align_row = QHBoxLayout()
        align_row.setSpacing(15)
        self._align_btns = []
        for icon, alignment, tip in [
            (_make_align_icon([18, 12, 16], "left"),   Qt.AlignmentFlag.AlignLeft,    "Align left"),
            (_make_align_icon([14, 18, 12], "center"), Qt.AlignmentFlag.AlignHCenter, "Center"),
            (_make_align_icon([16, 12, 18], "right"),  Qt.AlignmentFlag.AlignRight,   "Align right"),
            (_make_align_icon([18, 18, 18], "left"),   Qt.AlignmentFlag.AlignJustify, "Justify"),
        ]:
            btn = QToolButton()
            btn.setIcon(icon)
            btn.setIconSize(QSize(24, 24))
            btn.setToolTip(tip)
            btn.setCheckable(True)
            btn.setFixedSize(42, 42)
            btn.setObjectName("formatBtn")
            btn.clicked.connect(lambda _, a=alignment: self._apply_alignment(a))
            align_row.addWidget(btn)
            self._align_btns.append((btn, alignment))
        align_row.addStretch()
        layout.addLayout(align_row)

        layout.addStretch()

        self.format_dock = QDockWidget("Sidebar", self)
        self.format_dock.setObjectName("formatSidebarDock")
        self.format_dock.setWidget(panel)
        self.format_dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.format_dock.setMinimumWidth(220)
        self.format_dock.setMaximumWidth(300)
        self.format_dock.visibilityChanged.connect(self._sync_sidebar_action)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.format_dock)
        self.format_dock.hide()

    # ══════════════════════════════════════════════════════════════════════════
    # Action / widget factories
    # ══════════════════════════════════════════════════════════════════════════

    def _make_action(self, menu, label, shortcut=None, callback=None):
        act = QAction(label, self)
        if shortcut:
            act.setShortcut(shortcut)
        if callback:
            act.triggered.connect(callback)
        menu.addAction(act)
        return act

    def _make_tb_action(self, label, callback, tooltip="", checkable=False):
        act = QAction(label, self)
        act.setToolTip(tooltip)
        act.setCheckable(checkable)
        if callback:
            act.triggered.connect(callback)
        return act

    # ══════════════════════════════════════════════════════════════════════════
    # Safe editor proxies
    # ══════════════════════════════════════════════════════════════════════════

    def _editor_undo(self):
        ed = self.current_editor()
        if ed: ed.undo()
    def _editor_redo(self):
        ed = self.current_editor()
        if ed: ed.redo()
    def _editor_cut(self):
        ed = self.current_editor()
        if ed: ed.cut()
    def _editor_copy(self):
        ed = self.current_editor()
        if ed: ed.copy()
    def _editor_paste(self):
        ed = self.current_editor()
        if ed: ed.paste()

    # ══════════════════════════════════════════════════════════════════════════
    # Tab helpers
    # ══════════════════════════════════════════════════════════════════════════

    def current_editor(self) -> "CodeEditor | None":
        widget = self.tab_widget.currentWidget()
        return widget if isinstance(widget, CodeEditor) else None

    def create_tab(self, title="Untitled", path=None, content="", html=False):
        editor = CodeEditor()
        editor.setFont(QFont("Consolas", 13))
        editor.file_path = path
        editor._gutter_dark = (self._theme_mode != "light") if self._theme_mode != "auto" \
            else self._detect_system_dark()
        # Apply word-wrap state consistently
        if not getattr(self, "_word_wrap", True):
            editor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        doc = editor.document()
        if doc is not None:
            doc.setModified(False)
        if html:
            editor.setHtml(content)
        else:
            editor.setPlainText(content)

        _doc = editor.document()
        if _doc is not None:
            _doc.modificationChanged.connect(
                lambda _, ed=editor: self.update_tab_title(ed))
        editor.cursorPositionChanged.connect(self._update_status_bar)
        editor.cursorPositionChanged.connect(self.update_format_actions)
        editor.textChanged.connect(self._update_status_bar)

        index = self.tab_widget.addTab(editor, title)
        self.tab_widget.setCurrentIndex(index)
        self.update_window_title()
        return editor

    def _on_tab_changed(self, _index):
        self.update_window_title()
        self._update_status_bar()
        self.update_format_actions()

    def update_tab_title(self, editor: "CodeEditor"):
        index = self.tab_widget.indexOf(editor)
        if index < 0:
            return
        name = os.path.basename(editor.file_path) if editor.file_path else "Untitled"
        _doc = editor.document()
        if _doc is not None and _doc.isModified():
            name += "  \u25cf"
        self.tab_widget.setTabText(index, name)
        self.update_window_title()

    def update_window_title(self):
        editor = self.current_editor()
        if not editor:
            self.setWindowTitle("M-Pad")
            return
        name = editor.file_path if editor.file_path else "Untitled"
        _doc = editor.document()
        dot  = "\u25cf " if (_doc is not None and _doc.isModified()) else ""
        self.setWindowTitle(f"{dot}M-Pad  \u2014  {name}")

    # ══════════════════════════════════════════════════════════════════════════
    # Status bar
    # ══════════════════════════════════════════════════════════════════════════

    def _update_status_bar(self):
        editor = self.current_editor()
        if not editor:
            return
        cursor = editor.textCursor()
        line   = cursor.blockNumber() + 1
        col    = cursor.columnNumber() + 1
        self._status_pos.setText(f"Line {line},  Col {col}")
        # Update file label
        if hasattr(self, "_status_file"):
            self._status_file.setText(
                editor.file_path or "Untitled")
        # Defer expensive word/char count
        if hasattr(self, "_wc_timer"):
            self._wc_timer.start()

    def _do_word_count_update(self):
        """Debounced: update word and character counts in the status bar."""
        editor = self.current_editor()
        if not editor:
            return
        text  = editor.toPlainText()
        words = len(text.split()) if text.strip() else 0
        chars = len(text)
        self._status_words.setText(f"Words: {words}")
        if hasattr(self, "_status_chars"):
            self._status_chars.setText(f"Chars: {chars}")

    # ══════════════════════════════════════════════════════════════════════════
    # Explorer dock
    # ══════════════════════════════════════════════════════════════════════════

    def open_folder(self):
        path = QFileDialog.getExistingDirectory(
            self, "Open Folder", os.path.expanduser("~"))
        if path:
            self.file_model.setRootPath(path)
            self.tree_view.setRootIndex(self.file_model.index(path))
            if not self.file_dock.isVisible():
                self.file_dock.show()

    def on_tree_double_clicked(self, index):
        path = self.file_model.filePath(index)
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    contents = f.read()
                html = path.lower().endswith((".html", ".htm"))
                self.create_tab(title=os.path.basename(path), path=path,
                                content=contents, html=html)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not read file:\n{e}")

    def on_tree_context_menu(self, pos):
        index = self.tree_view.indexAt(pos)
        base_path = (self.file_model.filePath(index)
                     if index.isValid() else self.file_model.rootPath())
        if index.isValid() and os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)

        menu = QMenu(self)
        new_file_act   = QAction("New File",   self); menu.addAction(new_file_act)
        new_folder_act = QAction("New Folder", self); menu.addAction(new_folder_act)
        menu.addSeparator()
        rename_act = QAction("Rename", self); menu.addAction(rename_act)
        delete_act = QAction("Delete", self); menu.addAction(delete_act)

        vp = self.tree_view.viewport()
        exec_pos = vp.mapToGlobal(pos) if vp is not None else pos
        action = menu.exec(exec_pos)
        if   action == new_file_act:   self.create_new_file_in_dir(base_path)
        elif action == new_folder_act: self.create_new_folder_in_dir(base_path)
        elif action == rename_act and index.isValid(): self.rename_item(index)
        elif action == delete_act and index.isValid(): self.delete_item(index)

    def on_header_context_menu(self, pos):
        header = self.tree_view.header()
        if header is None:
            return
        menu   = QMenu(self)
        for col, label in COLUMN_LABELS.items():
            act = QAction(label, self)
            act.setCheckable(True)
            act.setChecked(not self.tree_view.isColumnHidden(col))
            act.setEnabled(col != COL_NAME)
            act.setData(col)
            menu.addAction(act)
        chosen = menu.exec(header.mapToGlobal(pos))
        if chosen is not None and chosen.data() is not None:
            self.tree_view.setColumnHidden(chosen.data(), not chosen.isChecked())

    def create_new_file_in_dir(self, dir_path):
        name, ok = QInputDialog.getText(self, "New File", "File name:")
        if ok and name:
            try:
                with open(os.path.join(dir_path, name), "w", encoding="utf-8"):
                    pass
                self.file_model.setRootPath(self.file_model.rootPath())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create file:\n{e}")

    def create_new_folder_in_dir(self, dir_path):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name:
            try:
                os.makedirs(os.path.join(dir_path, name), exist_ok=True)
                self.file_model.setRootPath(self.file_model.rootPath())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create folder:\n{e}")

    def rename_item(self, index):
        old_path = self.file_model.filePath(index)
        old_name = os.path.basename(old_path)
        new_name, ok = QInputDialog.getText(
            self, "Rename", "New name:", text=old_name)
        if ok and new_name and new_name != old_name:
            try:
                os.rename(old_path, os.path.join(os.path.dirname(old_path), new_name))
                self.file_model.setRootPath(self.file_model.rootPath())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not rename:\n{e}")

    def delete_item(self, index):
        path = self.file_model.filePath(index)
        res = QMessageBox.question(
            self, "Delete", f"Delete  \u2018{os.path.basename(path)}\u2019?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if res == QMessageBox.StandardButton.Yes:
            try:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
                self.file_model.setRootPath(self.file_model.rootPath())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete:\n{e}")

    # ══════════════════════════════════════════════════════════════════════════
    # File I/O
    # ══════════════════════════════════════════════════════════════════════════

    def new_file(self):
        self.create_tab()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", os.path.expanduser("~"), OPEN_FILTER)
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    contents = f.read()
                html = path.lower().endswith((".html", ".htm"))
                self.create_tab(title=os.path.basename(path), path=path,
                                content=contents, html=html)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not read file:\n{e}")

    def save_file(self):
        editor = self.current_editor()
        if not editor:
            return
        if not editor.file_path:
            self.save_file_as()
            return
        self._write_file(editor, editor.file_path)

    def save_file_as(self):
        editor = self.current_editor()
        if not editor:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", os.path.expanduser("~"), SAVE_FILTER)
        if path:
            editor.file_path = path
            self._write_file(editor, path)

    def _write_file(self, editor: "CodeEditor", path: str):
        try:
            with open(path, "w", encoding="utf-8") as f:
                if path.lower().endswith((".html", ".htm")):
                    f.write(editor.toHtml())
                else:
                    f.write(editor.toPlainText())
            _doc = editor.document()
            if _doc is not None:
                _doc.setModified(False)
            self.update_tab_title(editor)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")

    # ══════════════════════════════════════════════════════════════════════════
    # Formatting
    # ══════════════════════════════════════════════════════════════════════════

    def choose_font(self):
        editor = self.current_editor()
        if not editor:
            return
        font, ok = QFontDialog.getFont(editor.currentFont(), self, "Select Font")
        if ok:
            editor.setCurrentFont(font)

    def toggle_bold(self):
        editor = self.current_editor()
        if not editor:
            return
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if self.bold_action.isChecked()
                          else QFont.Weight.Normal)
        editor.mergeCurrentCharFormat(fmt)

    def toggle_italic(self):
        editor = self.current_editor()
        if not editor:
            return
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italic_action.isChecked())
        editor.mergeCurrentCharFormat(fmt)

    def toggle_underline(self):
        editor = self.current_editor()
        if not editor:
            return
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underline_action.isChecked())
        editor.mergeCurrentCharFormat(fmt)

    def _apply_font_family(self, font: QFont):
        editor = self.current_editor()
        if not editor:
            return
        fmt = QTextCharFormat()
        fmt.setFontFamilies([font.family()])
        editor.mergeCurrentCharFormat(fmt)

    def _apply_font_size(self, size: int):
        editor = self.current_editor()
        if not editor:
            return
        fmt = QTextCharFormat()
        fmt.setFontPointSize(float(size))
        editor.mergeCurrentCharFormat(fmt)

    def _apply_alignment(self, alignment):
        editor = self.current_editor()
        if not editor:
            return
        editor.setAlignment(alignment)
        for btn, al in self._align_btns:
            btn.setChecked(al == alignment)

    def update_format_actions(self):
        editor = self.current_editor()
        if not editor:
            return
        fmt = editor.currentCharFormat()
        self.bold_action.setChecked(fmt.fontWeight() == QFont.Weight.Bold)
        self.italic_action.setChecked(fmt.fontItalic())
        self.underline_action.setChecked(fmt.fontUnderline())

        if hasattr(self, "font_combo"):
            font = fmt.font()
            self.font_combo.blockSignals(True)
            self.font_size_spin.blockSignals(True)
            self.font_combo.setCurrentFont(font)
            pt = font.pointSize()
            if pt > 0:
                self.font_size_spin.setValue(pt)
            self.font_combo.blockSignals(False)
            self.font_size_spin.blockSignals(False)

        if hasattr(self, "_align_btns"):
            cur = editor.alignment()
            for btn, al in self._align_btns:
                btn.setChecked(al == cur)

    # ══════════════════════════════════════════════════════════════════════════
    # Dock toggles
    # ══════════════════════════════════════════════════════════════════════════

    def _toggle_explorer(self, checked): self.file_dock.setVisible(checked)
    def _toggle_sidebar(self, checked):  self.format_dock.setVisible(checked)

    def _sync_explorer_action(self, visible):
        if hasattr(self, '_explorer_tb_action'):
            self._explorer_tb_action.setChecked(visible)

    def _sync_sidebar_action(self, visible):
        if hasattr(self, '_sidebar_tb_action'):
            self._sidebar_tb_action.setChecked(visible)

    def _manual_save_layout(self):
        self._save_layout()
        _sb = self.statusBar()
        if _sb is not None:
            _sb.showMessage("Layout saved.", 3000)

    # ══════════════════════════════════════════════════════════════════════════
    # Word wrap & Zoom
    # ══════════════════════════════════════════════════════════════════════════

    def _toggle_word_wrap(self, checked: bool = False):
        """Toggle word-wrap on all open editors."""
        # Sync both the menu action and toolbar button
        if hasattr(self, "_wrap_action"):
            self._word_wrap = self._wrap_action.isChecked()
        if hasattr(self, "_wrap_tb_action"):
            self._wrap_tb_action.setChecked(self._word_wrap)
        if hasattr(self, "_wrap_action"):
            self._wrap_action.setChecked(self._word_wrap)

        mode = (QTextEdit.LineWrapMode.WidgetWidth
                if self._word_wrap
                else QTextEdit.LineWrapMode.NoWrap)
        for i in range(self.tab_widget.count()):
            ed = self.tab_widget.widget(i)
            if isinstance(ed, CodeEditor):
                ed.setLineWrapMode(mode)

    def _zoom_in(self):
        """Increase font size of the current editor by 1 pt."""
        editor = self.current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(min(font.pointSize() + 1, 144))
            editor.setFont(font)
            if hasattr(self, "font_size_spin"):
                self.font_size_spin.blockSignals(True)
                self.font_size_spin.setValue(font.pointSize())
                self.font_size_spin.blockSignals(False)

    def _zoom_out(self):
        """Decrease font size of the current editor by 1 pt."""
        editor = self.current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(max(font.pointSize() - 1, 6))
            editor.setFont(font)
            if hasattr(self, "font_size_spin"):
                self.font_size_spin.blockSignals(True)
                self.font_size_spin.setValue(font.pointSize())
                self.font_size_spin.blockSignals(False)

    def _zoom_reset(self):
        """Reset font size of the current editor to 13 pt."""
        editor = self.current_editor()
        if editor:
            font = editor.font()
            font.setPointSize(13)
            editor.setFont(font)
            if hasattr(self, "font_size_spin"):
                self.font_size_spin.blockSignals(True)
                self.font_size_spin.setValue(13)
                self.font_size_spin.blockSignals(False)

    # ══════════════════════════════════════════════════════════════════════════
    # Lifecycle
    # ══════════════════════════════════════════════════════════════════════════

    def close_tab(self, index: int):
        widget = self.tab_widget.widget(index)
        if widget is None:
            return
        if isinstance(widget, CodeEditor):
            _doc = widget.document()
            if _doc is not None and _doc.isModified():
                res = QMessageBox.question(
                    self, "Unsaved Changes",
                    "This tab has unsaved changes. Close it anyway?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No)
                if res == QMessageBox.StandardButton.No:
                    return
        self.tab_widget.removeTab(index)
        if self.tab_widget.count() == 0:
            self.new_file()

    def closeEvent(self, a0: QCloseEvent | None) -> None:  # type: ignore[override]
        modified: list[QWidget] = []
        for i in range(self.tab_widget.count()):
            w = self.tab_widget.widget(i)
            if w is not None:
                _doc = w.document() if isinstance(w, CodeEditor) else None  # type: ignore[attr-defined]
                if _doc is not None and _doc.isModified():
                    modified.append(w)
        if modified:
            res = QMessageBox.question(
                self, "Unsaved Changes",
                "Some tabs have unsaved changes. Exit anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No)
            if res == QMessageBox.StandardButton.No:
                if a0 is not None:
                    a0.ignore()
                return

        if self._prefs.get("restore_layout", True):
            self._save_layout()
        self._save_settings()

        if a0 is not None:
            a0.accept()

    # ══════════════════════════════════════════════════════════════════════════
    # About
    # ══════════════════════════════════════════════════════════════════════════

    def show_about_dialog(self):
        QMessageBox.about(
            self, "About M-Pad",
            "<h3>M-Pad v1.2</h3>"
            "<p>A lightweight text companion.</p>"
            "<hr>"
            "<p><b>Created by</b>: <i>Miran Kljun</i></p>"
            "<p><b>Git</b>: <i>@themix88</i></p>"
            "<p><b>E-Mail</b>: <i>miran.kljun@gmail.com</i></p>"
            "<hr>"
            "<p><b>License</b>: <i>GPLv3 (c) 2026</i></p>",
        )


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    notepad = PlainNotepad()
    notepad.show()
    sys.exit(app.exec())