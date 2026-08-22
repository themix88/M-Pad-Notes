# Changelog

All notable changes to the M-Pad project will be documented in this file.

## [1.3] - 2026-08-22

### Added
- **Aether theme** — new theme option that reads colors from the active [Omarchy](https://github.com/basecamp/omarchy) palette (`~/.config/aether/theme/colors.toml`, falling back to `~/.local/state/omarchy/current/theme/colors.toml`). Generates a full application QSS dynamically from the palette, supporting both dark and light modes.
- **Live theme reloading** — a `QFileSystemWatcher` monitors the Aether colors file and reapplies the theme automatically whenever the palette changes, without needing to restart the app.
- `fontpkg-jetbrains-mono` added to `requirements.txt`.

### Changed
- Default editor font changed to **JetBrains Mono** (falls back to SF Pro Text → Inter → Segoe UI → Ubuntu → system-ui).

## [1.2] - 2026-08-16

### Added
- **Word Wrap toggle** — new `View → Word Wrap` menu item (`Ctrl+Shift+W`) and `↩ Wrap` toolbar button; setting applies to all open tabs and is respected by new tabs.
- **Zoom In / Zoom Out / Reset Zoom** — `View` menu entries with standard shortcuts (`Ctrl++`, `Ctrl+-`, `Ctrl+0`); `−` and `+` toolbar buttons also added. Zoom syncs with the Format Sidebar font-size spinner.
- **Character count** in the status bar alongside the existing word count (`Chars: N`).
- **File path label** on the left side of the status bar showing the path of the current file.
- Status bar label separators — subtle vertical dividers between status items, styled via QSS.

### Changed
- **Explorer dock moved back to the Left side** (reverts the v1.1 change to Bottom placement — left side is the standard convention for file explorers).
- **Word count is now debounced** (400 ms delay after last keystroke) to avoid expensive recalculation on every keypress in large documents.
- Text editor now has `padding: 4px 8px` in both themes for more comfortable reading.
- Status bar `min-height` set to `24 px`; label text opacity slightly increased for better readability.
- Removed redundant per-label `setStyleSheet()` calls from the status bar builder — styling is now fully managed by the application QSS.
- Consolidated three separate `from PyQt6.QtGui import` statements into one clean block.
- `About` dialog version string updated to v1.2.

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
- Explorer dock opens from the **bottom** of the window by default (later reverted to left side in v1.2).
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

## [1.0] - 2026-07-13

Initial release of M-Pad v1.0, a lightweight text companion built using Python and PyQt6.
