# M-Pad

M-Pad is a lightweight, blazing-fast text companion built using Python and PyQt6.

## Features

* **UI:** Initial styling with seamless light, dark, and auto theme switching. <-- Theme will be improved in future releases. Basics work.
* **Tabbed Interface:** Work on multiple files simultaneously with intelligent save prompts. <-- Just fancy wording. It basicly gives you a warning to save before closing the tab of file.
* **Integrated Explorer:** A left-docked file tree (hidden by default) for quick access to your system. Can be dragged and dropped.
* **Formatting Sidebar:** A right-docked properties panel for rich text styling (Font, Size, Alignment, Bold, Italic, Underline). Can be dragged and dropped.
* **Line Numbers:** Sticky code-editor-style line numbers that adapt perfectly to the current theme.
* **Native Integration:** Fully utilizes PyQt6 for native-feeling file dialogs and keyboard shortcuts.

## Prerequisites

* Python 3.6 or higher
* PyQt6 (`python-pyqt6` on Arch Linux)

## Running Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/themix88/M-Pad.git
   cd M-Pad
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

## Packaging for Arch Linux

This repository contains a `PKGBUILD` and `.desktop` file for creating a native Arch Linux package.

1. Create the package:
   ```bash
   makepkg -si
   ```
   *This will automatically resolve dependencies, build the package, and install `m-pad` to your system.*

2. You can now launch M-Pad from your desktop environment's application launcher or by running `m-pad` in your terminal.

## License

Released under the GPLv3 License. (c) 2026 Miran Kljun