- [🟡 Shortcuts ](#-shortcuts-)
  - [General](#general)
  - [Panels \& layout](#panels--layout)
  - [Editing](#editing)
  - [Markdown files](#markdown-files)

<br><br>

# 🟡 Shortcuts <br>

<br>

## General

| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+P` | Opens the **Command Palette**: search for any VS Code command. The heart of control: type a command name (e.g. `Python: Select Interpreter`) and run it without digging through menus. |
| `Ctrl+N` | Creates a new (unsaved) file. |
| `Ctrl+R` | **Open Recent**: quickly reopens recent folders / workspace files. |
| `Ctrl+K` → `Ctrl+S` | Opens the **Keyboard Shortcuts** editor: a searchable list of all shortcuts. Search by command name (e.g. `format`) or by the keys themselves, and change any shortcut by double-clicking it. Hold `Ctrl`, press `K`, then `S`. |

<br>

## Panels & layout

| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+E` | Switches to the **Explorer** (left panel with the file/folder tree). |
| `Ctrl+Shift+G` | Opens the **Source Control** panel: stage changes, write commit messages, commit and sync (push/pull) to GitHub. Shows which files changed. |
| `Ctrl+B` | Toggles the side bar (Explorer etc.). Hide it to get more space for editing. |
| `` Ctrl+` `` | Toggles the integrated terminal. |
| `Ctrl+K` → `W` | Closes **all open tabs** (editors) in the current editor group. If you have the editor split, the other side stays open. For files with unsaved changes, VS Code asks whether to save them first. Two-step shortcut: press `Ctrl+K`, release, then `W`. |
| `Fn+F11` | Toggles **full screen**: VS Code fills the whole screen, without the window title bar and the Windows taskbar. Press it again to go back. On a laptop the `F` keys often control brightness, volume etc. by default, so you need `Fn`; on a regular keyboard plain `F11` is enough. |

<br>

## Editing

| Shortcut | What it does |
| --- | --- |
| `Alt+↑` / `Alt+↓` | Moves the current line up / down. With several lines selected, moves all of them at once. No need to cut and paste. |
| `Ctrl+L` | Selects the whole current line. Press it again to add the next line to the selection, and so on. |
| `Ctrl+Shift+L` | Selects **all occurrences** of the selected text in the file and puts a cursor on each one, so you can edit them all at once (e.g. rename a variable everywhere in the file). Select the text first, or just place the cursor in a word. |
| `Shift+Alt+F` | **Formats the whole file**: fixes indentation, spacing and line breaks according to the language's rules. Works only when a formatter for that file type is available: built in for JSON, HTML, CSS and JavaScript; for Python you need a formatter extension (e.g. Black or Ruff). The first time, VS Code may ask which formatter to use. |

<br>

## Markdown files

| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+V` | Opens the rendered preview of a `.md` file (replaces the editor with the preview). |
| `Ctrl+K` → `V` | Opens the preview **to the side** (split): edit on the left, see the result live on the right. It's a two-step shortcut: press `Ctrl+K`, release, then `V`. |

<br>
