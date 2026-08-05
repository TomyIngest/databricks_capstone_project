- [VS Code Shortcuts](#vs-code-shortcuts)
  - [Command Palette](#command-palette)
  - [Files and panels](#files-and-panels)
  - [Markdown preview](#markdown-preview)
- [Command Line prompts for Project](#command-line-prompts-for-project)
  - [Install Python](#install-python)
  - [Check versions](#check-versions)
  - [Install packages into a specific Python](#install-packages-into-a-specific-python)

<br>
<br>

# VS Code Shortcuts
<br>

## Command Palette

| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+P` | Opens the Command Palette: search for any VS Code command. The heart of control: type a command name (e.g. `Python: Select Interpreter`) and run it without digging through menus. |

<br><br>

## Files and panels

| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+E` | Switches to the Explorer (left panel with the file/folder tree). |
| `Ctrl+N` | Creates a new (unsaved) file. |
| `Ctrl+R` | Open Recent — quickly reopen recent folders / workspace files. |

<br><br>

## Markdown preview


| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+V` | Opens the rendered preview of a `.md` file (replaces the editor with the preview). |
| `Ctrl+K` → `V` | Opens the preview **to the side** (split): edit on the left, see the result live on the right. It's a two-step shortcut — press `Ctrl+K`, release, then `V`. |

<br><br><br>

# Command Line prompts for Project
<br>

## Install Python

| Command | What it does |
| --- | --- |
| `winget install Python.Python.3.12` | Installs the latest Python 3.12.x with binaries and sets up PATH automatically. |

<br><br>

## Check versions


| Command | What it does |
| --- | --- |
| `python --version` | Prints the version of the default Python (the one on PATH). |
| `py --list` | Lists all installed Python versions via the `py` launcher. |

<br><br>

## Install packages into a specific Python

| Command | What it does |
| --- | --- |
| `py -3.12 -m pip install pandas` | Installs the latest pandas into Python 3.12 specifically. |
| `py -3.12 -m pip install pandas==2.2.3` | Installs an exact version (e.g. to match DBR 18). |
| `py -3.12 -m pip show pandas` | Shows the installed version and where it landed — confirms it went into 3.12. |

---

