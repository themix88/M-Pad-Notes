# M-Pad

![Version](https://img.shields.io/badge/version-1.2-blue.svg)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![PyQt Version](https://img.shields.io/badge/PyQt-6-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)

M-Pad is a lightweight, blazing-fast, and customizable tabbed text companion built using Python and PyQt6. It provides a clean environment for formatting rich text and managing files in a single seamless workspace.

---

## 🚀 Features

* **🎨 UI:** Seamless light, dark, and auto theme switching. Theme adapts to system preference when set to Auto.
* **📂 Tabbed Interface:** Work on multiple files simultaneously with intelligent save prompts. (It's just fancy wording, it asks you to save before closing the files)
* **🌳 Integrated File Explorer:** Left-docked interactive directory tree for rapid system navigation, supporting drag-and-drop layout configuration. Dock visibility and position can be saved between sessions.
* **📝 Rich Formatting Sidebar:** Right-docked panel for styling (font family, size, alignment, bold, italic, and underline). Also supports drag-and-drop layout configuration.
* **🔢 Line Numbers:** Sticky, editor-style line numbering that automatically adapts to the selected theme.
* **↩ Word Wrap:** Toggle word-wrap on all open editors via `View → Word Wrap` (`Ctrl+Shift+W`) or the toolbar button.
* **🔍 Zoom:** Increase/decrease editor font size with `Ctrl++` / `Ctrl+-` / `Ctrl+0` (Reset), or the `−` and `+` toolbar buttons. Syncs with the Format Sidebar font-size spinner.
* **📊 Status Bar:** Shows current line/column, word count, character count, and file path. Word/character counts are debounced for performance on large files.
* **⌨️ Keyboard Shortcuts:** Intuitive shortcuts for all common actions, including file operations, formatting, dock toggling, word wrap, and zoom. All shortcuts are displayed in menu items and tooltips.

---

## 🛠️ Prerequisites and Dependencies

This application requires:
* **Python 3.6 or higher**
* **PyQt6**

### Installing PyQt6

Depending on your workflow, you can install PyQt6 using one of the following methods:

#### Option A: Via `pip` (Cross-platform / Recommended for development)
Install the dependencies directly into your environment:
```bash
pip install -r requirements.txt
```
*(Or manually run `pip install PyQt6`)*

#### Option B: Via Linux Package Managers
You can install PyQt6 directly through your system package repository:
* **Arch Linux:** `sudo pacman -S python-pyqt6`
* **Debian/Ubuntu:** `sudo apt install python3-pyqt6`
* **Fedora:** `sudo dnf install python3-pyqt6`

---

## 💻 Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/themix88/M-Pad-Notes.git
   cd M-Pad-Notes
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application:**
   ```bash
   python main.py
   ```

---

## 📦 Packaging for Arch Linux

This repository contains a `PKGBUILD` and `m-pad.desktop` file to build and install a native Arch Linux package.

1. **Build and install:**
   ```bash
   makepkg -si
   ```
   *Note: `makepkg` will automatically download and install `python` and `python-pyqt6` dependencies from the official repositories; no manual setup is required beforehand.*

2. **Launch:** Run `m-pad` in the terminal or launch M-Pad from your desktop application launcher.

---

## 📄 License

This project is released under the GPLv3 License.

&copy; 2026 Miran Kljun