# Changelog

All notable changes to the M-Pad project will be documented in this file.

## [1.0] - 2026-07-13

Initial release of M-Pad v1.0, a lightweight text companion built using Python and PyQt6.

## [1.1] - 2026-08-14

### Added
- Added `requirements.txt` to track required Python dependencies (`PyQt6`).
- Enhanced `README.md` with explicit details on how to install prerequisites using `pip` and system package managers (Arch, Debian/Ubuntu, Fedora).
- Added clarification on how Arch Linux packaging (`PKGBUILD`) resolves and installs dependencies automatically.
- New **View** menu with **Explorer** (`Ctrl+Shift+E`) and **Format Sidebar** (`Ctrl+Shift+F`) toggle entries.
- Explorer keyboard shortcut `Ctrl+Shift+E` is now properly bound (was previously only displayed in the tooltip).
- Added additional, always visible, shortcut hints to menu items.
- Opening a folder via **File → Open Folder** now automatically shows the Explorer dock.
- State saving for Explorer and Format Sidebar docks (open/closed state is now remembered between sessions). Can be toggled as well.
- Layout saving for Explorer and Format Sidebar docks (position and size is now remembered between sessions). Can be toggled as well.

### Changed
- Explorer dock now opens from the **bottom** of the window by default (was left side).
- Renamed top-level **About** menu to **Help** (standard convention).
- Reordered internal widget construction so dock widgets are built before menus, enabling the View menu to use Qt's native `toggleViewAction()` for reliable state synchronisation.
- Removed font formatting buttons from the toolbar (these are now accessible via the Format Sidebar or shortcuts).
- Removed New, open and save buttons from the toolbar (these are now accessible via the File menu or shortcuts).
- Shortcuts for Explorer and Format Sidebar docks are now displayed in the menu tooltips (previously only displayed in the dock tooltips).
- Shortcuts for Explorer and Format Sidebar docks changed to `Ctrl+Shift+E` and `Ctrl+Shift+F` respectively. Far easier to remember and less likely to conflict with other shortcuts. Tooltips updated accordingly.
- Alignment fonts are now displayed in the Format Sidebar as icons instead of text (more intuitive).

### Fixed
- Fixed a bug where the Explorer dock would not open when a folder was selected via **File → Open Folder**.
- Fixed a bug where theme, if set to auto, would not update when the system theme changed (now updates on window focus).

### Known Issues / Bugs
- Sidebar dock, when dragged to the top or bottom of the window, will not resize properly when the window is resized. Will probably restrict it to left/right docking in future releases.
