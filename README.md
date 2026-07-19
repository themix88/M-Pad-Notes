# M-Pad

![Version](https://img.shields.io/badge/version-1.1-blue.svg)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![PyQt Version](https://img.shields.io/badge/PyQt-6-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)

M-Pad is a lightweight, blazing-fast, and customizable tabbed text companion built using Python and PyQt6. It provides a clean environment for formatting rich text and managing files in a single seamless workspace.

---

## 🚀 Features

* **🎨 UI:** Initial styling with seamless light, dark, and auto theme switching. <-- Theme will be improved in future releases. Basics work.
* **📂 Tabbed Interface:** Work on multiple files simultaneously with intelligent save prompts. <-- Just fancy wording. It basicly gives you a warning to save before closing the tab of file.
* **🌳 Integrated File Explorer:** Bottom-docked interactive directory tree for rapid system navigation, supporting drag-and-drop layout configuration. States of which, can be saved or not, your choice.
* **📝 Rich Formatting Sidebar:** Right-docked panel for styling (Font family, size, alignment, bold, italic, and underline settings). Also supports drag-and-drop layout configuration.
* **🔢 Line Numbers:** Sticky, editor-style line numbering that automatically adapts to the selected theme.
* **⌨️ Keyboard Shortcuts:** Intuitive shortcuts for common actions (actually standard practice...), including file operations, formatting, and dock toggling. All shortcuts are displayed in tooltips for easy reference. Might add changing of shortcuts in future releases, but for now, you can just use the defaults.

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