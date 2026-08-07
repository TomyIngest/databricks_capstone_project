- [VS Code Shortcuts](#vs-code-shortcuts)
  - [Command Palette](#command-palette)
  - [Files and panels](#files-and-panels)
  - [Markdown preview](#markdown-preview)
- [Command Line prompts](#command-line-prompts)
  - [Install Python](#install-python)
  - [Check versions](#check-versions)
  - [Install packages into a specific Python](#install-packages-into-a-specific-python)
- [Databricks](#databricks)
  - [Databricks CLI Commands](#databricks-cli-commands)
  - [databricks YAML (DAB structure)](#databricks-yaml-dab-structure)
    - [`bundle`](#bundle)
    - [`include`](#include)
  - [PowerShell helpers](#powershell-helpers)
    - [List clusters across all profiles](#list-clusters-across-all-profiles)

<br>
<br>

# VS Code Shortcuts
<br>

## Command Palette

| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+P` | Opens the Command Palette: search for any VS Code command. The heart of control: type a command name (e.g. `Python: Select Interpreter`) and run it without digging through menus. |
| `Ctrl+Shift+G` | Opens the Source Control panel — stage changes, write commit messages, commit, and sync (push/pull) to GitHub. Shows which files changed. |

<br><br>

## Files and panels

| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+E` | Switches to the Explorer (left panel with the file/folder tree). |
| `Ctrl+N` | Creates a new (unsaved) file. |
| `Ctrl+R` | Open Recent — quickly reopen recent folders / workspace files. |
| `Ctrl+B` | Toggle the side bar (Explorer etc.) — hide it to get more editing space. |
| `` Ctrl+` `` | Toggle the integrated terminal. |

<br><br>

## Markdown preview


| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+V` | Opens the rendered preview of a `.md` file (replaces the editor with the preview). |
| `Ctrl+K` → `V` | Opens the preview **to the side** (split): edit on the left, see the result live on the right. It's a two-step shortcut — press `Ctrl+K`, release, then `V`. |

<br><br><br>

# Command Line prompts
<br>

## Install Python

| Command | What it does |
| --- | --- |
| `winget install Python.Python.3.12` | Installs the latest Python 3.12.x with binaries and sets up PATH automatically. |
| `py -3.11 -m venv .venv_a` | Creates a virtual environment named `.venv_a` using Python 3.11. `py -3.11` = that specific Python, `-m venv` = run the built-in venv module, `.venv_a` = the folder it creates. Activate it with `.venv_a\Scripts\activate`. The leading dot makes it a hidden file/folder — handy so it stays out of the way and is easy to keep out of the git repo (via `.gitignore`). |
| `.venv_a\Scripts\activate` | Activates the virtual environment. After it, the prompt shows `(.venv_a)` and `python` / `pip` point at that venv. Deactivate with `deactivate`. |

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

<br><br><br>

# Databricks 
<br>

## Databricks CLI Commands

| Command | What it does |
| --- | --- |
| `databricks --help` (or `-h`) | Shows the top-level help — lists all available command groups and global options. |
| `databricks <command> --help` (or `-h`) | Shows help for a specific command (its subcommands, flags, usage). E.g. `databricks clusters --help`. |
| `databricks configure --host <workspace URL>` | Sets up authentication to a workspace — points the CLI at your Databricks host, then prompts for a token. Stores it in the config so later commands know which workspace to talk to. |
| `databricks auth profiles` | Lists all configured authentication profiles and their status (host, whether auth is valid). Handy when you connect to multiple workspaces — each profile is a named set of credentials in `~/.databrickscfg`. |
| `databricks auth describe` | Shows the details of the currently active auth configuration — which host, profile, and auth method (token, OAuth) the CLI is using right now. Good for confirming you're pointed at the workspace you think you are. |
| `databricks clusters create --json @compute-setup.json --profile Data_Engineering_001` | Creates a cluster from the JSON definition in `compute-setup.json`, targeting the Data_Engineering_001 profile. `@` = read JSON from that file. |
| `databricks clusters delete <cluster-id> --profile <name>` | Terminates a cluster (shuts it down). The cluster definition stays — you can start it again later. This is a stop, not a permanent removal. |
| `databricks clusters permanent-delete <cluster-id> --profile <name>` | Permanently deletes a cluster — removes it from the workspace entirely, including its definition. Cannot be started again. Irreversible. |
| `databricks bundle init --profile Data_Engineering_001` | Creates a new Databricks Asset Bundle — pick a template, answer a few prompts, and it scaffolds the project. |
| `databricks bundle validate` | Validates the bundle — checks `databricks.yml` for errors before deploying. Must be run from the bundle's root directory (where `databricks.yml` lives); it picks up the target/profile from there, so no `--profile` needed. |
| `databricks bundle deploy` | Deploys the bundle to the target workspace — uploads the resources and creates/updates the jobs, pipelines etc. defined in `databricks.yml`. Run from the bundle's root directory; it uses the target/profile from `databricks.yml`. Add `-t <target>` (or `--target <target>`) to pick which target/workspace to deploy to — the targets are defined in `databricks.yml` (e.g. `dev`, `prod`), each pointing at a workspace. |
| `databricks bundle destroy` | Tears down the deployed bundle — removes the resources (jobs, pipelines etc.) it created in the target workspace. Run from the bundle's root directory; add `-t <target>` to pick which target/workspace to destroy in. Asks for confirmation before deleting. |

<br><br>

## databricks YAML (DAB structure)


### `bundle`
```yaml
bundle:
  name: DAB_Project
  uuid: 27dfbc1c-...
```
- Identifies the bundle. `name` is used as a prefix for deployed resources; `uuid` is auto-generated by `bundle init` — leave it.

### `include`
```yaml
include:
  - resources/*.yml
```
- Tells the bundle which YAML files to load and merge — this is how you modularize (split jobs/pipelines into separate files under `resources/`).
- `*` = files directly in the folder only. `resources/*/*.yml` = exactly one subfolder level deep. `resources/**/*.yml` = any depth, recursive (picks up all subfolders). Use `**` when modularizing into nested folders.


## PowerShell helpers

Small PowerShell snippets that wrap the Databricks CLI to do things across profiles.

### List clusters across all profiles

```powershell
databricks auth profiles -o json | ConvertFrom-Json |
  Select-Object -ExpandProperty profiles |
  ForEach-Object {
    Write-Host "=== $($_.name) ===" -ForegroundColor Cyan
    databricks clusters list --profile $_.name
  }
```

- Reads all configured profiles as JSON, then loops over each one and lists its clusters.
- `-o json` = output as JSON (so `ConvertFrom-Json` can turn it into objects).
- `$_` = the current profile in the loop; `$_.name` = its name.
- Note: serverless workspaces have no all-purpose clusters, so those profiles return empty. For serverless SQL compute use `databricks warehouses list` instead.
