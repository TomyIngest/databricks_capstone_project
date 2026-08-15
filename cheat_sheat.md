- [🟡 VS Code ](#-vs-code-)
  - [`Shortcuts`](#shortcuts)
- [🟡 Command Line prompts](#-command-line-prompts)
  - [Install Python \& Configure Virtual Environments](#install-python--configure-virtual-environments)
  - [Check versions](#check-versions)
  - [Install packages into a specific Python](#install-packages-into-a-specific-python)
  - [Python interactive (terminal)](#python-interactive-terminal)
- [🟡 Python](#-python)
  - [System commands](#system-commands)
- [🟡 Databricks Asset Bundles](#-databricks-asset-bundles)
  - [Databricks CLI Commands](#databricks-cli-commands)
  - [databricks YAML (DAB structure)](#databricks-yaml-dab-structure)
    - [`bundle`](#bundle)
    - [`include`](#include)
    - [`targets`](#targets)
  - [Running python with Databricks Connect via terminal](#running-python-with-databricks-connect-via-terminal)
  - [PowerShell helpers](#powershell-helpers)
    - [List clusters across all profiles](#list-clusters-across-all-profiles)
- [🟡 Data Engineering](#-data-engineering)
  - [Concepts](#concepts)
    - [`Lakeflow Spark Declarative Pipelines (SDP)`](#lakeflow-spark-declarative-pipelines-sdp)
      - [**`SQL`**](#sql)
        - [**Streaming table from Auto Loader (`read_files`)**](#streaming-table-from-auto-loader-read_files)
        - [**Streaming table from another pipeline table (`STREAM(table)`)** — between layers (bronze → silver)](#streaming-table-from-another-pipeline-table-streamtable--between-layers-bronze--silver)
        - [**Materialized view** (batch — no `STREAM`)](#materialized-view-batch--no-stream)
        - [**Expectations / constraints — `ON VIOLATION` actions**](#expectations--constraints--on-violation-actions)
        - [**Schema options inside `read_files(...) only`** — format `option => 'value'`](#schema-options-inside-read_files-only--format-option--value)
        - [**Full reference — everything usable on a streaming table**](#full-reference--everything-usable-on-a-streaming-table)
        - [**`CREATE FLOW`** — separate the target table from the flow(s) that write into it](#create-flow--separate-the-target-table-from-the-flows-that-write-into-it)
      - [**`Python`**](#python)
        - [**Full reference — everything usable on a streaming table (Python)**](#full-reference--everything-usable-on-a-streaming-table-python)
        - [**`CREATE FLOW` (Python)** — multiple sources into one streaming table (fan-in)](#create-flow-python--multiple-sources-into-one-streaming-table-fan-in)
        - [**Overview of `dp.methods`**](#overview-of-dpmethods)
    - [`Auto Loader`](#auto-loader)
    - [`Delta Sharing`](#delta-sharing)
      - [Provider setup (D2D / Unity Catalog)](#provider-setup-d2d--unity-catalog)
      - [Provider setup (off Databricks / open-source server)](#provider-setup-off-databricks--open-source-server)
    - [`Query Federation (Lakehouse Federation)`](#query-federation-lakehouse-federation)
    - [`Pipeline execution modes (Lakeflow Declarative Pipelines)`](#pipeline-execution-modes-lakeflow-declarative-pipelines)
  - [Spark SQL](#spark-sql)
  - [PySpark](#pyspark)
  - [Databricks-specific vs open-source Spark](#databricks-specific-vs-open-source-spark)
- [🟡 Additional Information on Databricks Platform](#-additional-information-on-databricks-platform)
  - [Debugging](#debugging)
  - [Optimization](#optimization)
    - [Predicate pushdown](#predicate-pushdown)
    - [Column pruning](#column-pruning)
    - [Partitioning](#partitioning)
    - [Liquid clustering](#liquid-clustering)
    - [OPTIMIZE](#optimize)
    - [OPTIMIZE: partitioning vs liquid clustering](#optimize-partitioning-vs-liquid-clustering)
    - [VACUUM](#vacuum)

<br><br>

# 🟡 VS Code <br>

## `Shortcuts` 
<br>

| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+P` | Opens the Command Palette: search for any VS Code command. The heart of control: type a command name (e.g. `Python: Select Interpreter`) and run it without digging through menus. |
| `Ctrl+Shift+G` | Opens the Source Control panel — stage changes, write commit messages, commit, and sync (push/pull) to GitHub. Shows which files changed. |
| `Ctrl+Shift+V` | Opens the rendered preview of a `.md` file (replaces the editor with the preview). |
| `Ctrl+K` → `V` | Opens the preview **to the side** (split): edit on the left, see the result live on the right. It's a two-step shortcut — press `Ctrl+K`, release, then `V`. |
| `Ctrl+Shift+E` | Switches to the Explorer (left panel with the file/folder tree). |
| `Ctrl+N` | Creates a new (unsaved) file. |
| `Ctrl+R` | Open Recent — quickly reopen recent folders / workspace files. |
| `Ctrl+B` | Toggle the side bar (Explorer etc.) — hide it to get more editing space. |
| `` Ctrl+` `` | Toggle the integrated terminal. |



<br><br>

# 🟡 Command Line prompts

<br>

## Install Python & Configure Virtual Environments 

| Command | What it does |
| --- | --- |
| `winget install Python.Python.3.12` | Installs the latest Python 3.12.x with binaries and sets up PATH automatically. |
| `py -3.11 -m venv .venv_a` | Creates a virtual environment named `.venv_a` using Python 3.11. `py -3.11` = that specific Python, `-m venv` = run the built-in venv module, `.venv_a` = the folder it creates. Activate it with `.venv_a\Scripts\activate`. The leading dot makes it a hidden file/folder — handy so it stays out of the way and is easy to keep out of the git repo (via `.gitignore`). |
| `.venv_a\Scripts\activate` | Activates the virtual environment. After it, the prompt shows `(.venv_a)` and `python` / `pip` point at that venv. Deactivate with `deactivate`. |
| `deactivate` | Deactivates the current virtual environment. The `(.venv_a)` prefix disappears from the prompt and `python` / `pip` point back at the global Python. |
| `pip install databricks-connect==18` | Installs Databricks Connect v18 into the active venv — matches serverless environment version 5 (Python 3.12, Connect 18). Lets you run Spark code from VS Code against Databricks compute. Connect version must be ≤ the serverless environment's runtime; check `environment_version` in the job YAML (5→18, 4→17.3) and match it. |

<br>

## Check versions


| Command | What it does |
| --- | --- |
| `python --version` | Prints the version of the default Python (the one on PATH). |
| `py --list` | Lists all installed Python versions via the `py` launcher. |

<br>

## Install packages into a specific Python

| Command | What it does |
| --- | --- |
| `py -3.12 -m pip install pandas` | Installs the latest pandas into Python 3.12 specifically. |
| `py -3.12 -m pip install pandas==2.2.3` | Installs an exact version (e.g. to match DBR 18). |
| `py -3.12 -m pip show pandas` | Shows the installed version and where it landed — confirms it went into 3.12. |

<br>

## Python interactive (terminal)

| Command | What it does |
| --- | --- |
| `python` | Starts the interactive Python prompt in the terminal. |
| `exit()` | Exits the interactive Python prompt, back to the terminal. |
| `python skript.py` | Runs a Python file with the active interpreter (activate the venv first to use it). |

<br><br><br>

# 🟡 Python

<br>

## System commands

Python's `sys` module — interacting with the interpreter and runtime environment.

| Command | What it does |
| --- | --- |
| `sys.path.append("path")` | Adds a folder to Python's module search path at runtime, so you can import modules from a location that isn't normally on the path. Needs `import sys` first. E.g. `sys.path.append("../src")` to import shared/local modules from another folder. |
| `os.getcwd()` | Returns the current working directory as a string (the folder the Python process is running from). `os` = built-in module, import it first with `import os`. Handy for building relative paths or checking where a script is executing. |
| `os.path.abspath(path)` | Returns the absolute (full) path of a relative path — resolves it against the current working directory. E.g. `os.path.abspath("data.csv")` → `/home/user/project/data.csv`. |
| `os.path.join(a, b, ...)` | Joins path parts into one path using the correct separator for the OS (`/` on Linux/Mac, `\` on Windows). E.g. `os.path.join("folder", "sub", "file.csv")`. Safer than manually gluing strings with slashes. |

<br><br><br>

# 🟡 Databricks Asset Bundles

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

### `targets`
```yaml
targets:
  dev:
    mode: development
    workspace:
      host: https://adb-....azuredatabricks.net
      root_path: /Workspace/Users/<user>/.bundle/${bundle.name}/${bundle.target}
```

- Defines where the bundle deploys — without `targets`, deployment can't work. Deploy with `databricks bundle deploy -t <target>`.
- Minimum per target: the **name** (`dev`, or `<company>_<env>` like `acme_dev` for multiple clients), **`mode`**, and **`workspace.host`**.
- `mode` = `development` (resources prefixed `[dev name]`, schedules paused) or `production` (runs for real, no prefixes).
- `workspace.host` = which workspace to target; pairs with the profile in `.databrickscfg` (same host) for auth.
- `workspace.root_path` = where in the workspace the bundle files are stored. `${bundle.name}` and `${bundle.target}` are auto-filled, so each bundle/target gets its own isolated path (no clashes). Optional — auto-generated if omitted.

<br><br>

## Running python with Databricks Connect via terminal

Run Spark from a script (`python file.py`). Independent of the Databricks extension panel; reads only what you pass + `.databrickscfg`. Must run from the venv that has `databricks-connect` installed.

```python
from databricks.connect import DatabricksSession

# serverless
spark = DatabricksSession.builder.profile("Data_Engineering_001").serverless(True).getOrCreate()

# specific cluster
spark = DatabricksSession.builder.profile("Data_Engineering_001").clusterId("<cluster-id>").getOrCreate()
```

- Profile required (no DEFAULT). Avoid it in code by setting `$env:DATABRICKS_CONFIG_PROFILE = "Data_Engineering_001"` first.
- `databricks-connect` lives in the venv, not global Python — activate the venv or you get `No module named 'databricks'`.

<br><br>

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
<br><br><br>

# 🟡 Data Engineering
<br>

## Concepts

<br>

### `Lakeflow Spark Declarative Pipelines (SDP)`

Declarative framework for batch & streaming ETL in SQL/Python. **DLT → Lakeflow (Spark) Declarative Pipelines / SDP** — DLT (Delta Live Tables) was the original name, now Lakeflow pipelines. Old DLT code runs without migration. Terminology on the test: DLT = old name, Lakeflow pipelines / SDP = current. Auto Loader inside SDP is `read_files()` (replaced the old `cloud_files()`); schema and checkpoint dirs are managed automatically by the framework.

#### **`SQL`**

##### **Streaming table from Auto Loader (`read_files`)**
```sql
CREATE OR REFRESH STREAMING TABLE bronze_orders(
  CONSTRAINT valid_id     EXPECT (id IS NOT NULL),                                 -- warn
  CONSTRAINT valid_amount EXPECT (amount >= 0)        ON VIOLATION DROP ROW,       -- drop
  CONSTRAINT valid_date   EXPECT (order_date IS NOT NULL) ON VIOLATION FAIL UPDATE -- fail
) AS
SELECT *
FROM STREAM read_files('/path/to/landing', format => 'json');
```

##### **Streaming table from another pipeline table (`STREAM(table)`)** — between layers (bronze → silver)
```sql
CREATE OR REFRESH STREAMING TABLE silver_orders(
  CONSTRAINT valid_id     EXPECT (id IS NOT NULL),                           -- warn
  CONSTRAINT valid_amount EXPECT (amount >= 0)  ON VIOLATION DROP ROW,       -- drop
  CONSTRAINT valid_cust   EXPECT (customer_id IS NOT NULL) ON VIOLATION FAIL UPDATE -- fail
) AS
SELECT * FROM STREAM(bronze_orders);
```

##### **Materialized view** (batch — no `STREAM`)
```sql
CREATE OR REFRESH MATERIALIZED VIEW orders_summary(
  CONSTRAINT valid_total EXPECT (total IS NOT NULL),                    -- warn
  CONSTRAINT non_neg     EXPECT (total >= 0)  ON VIOLATION DROP ROW,    -- drop
  CONSTRAINT has_cust    EXPECT (customer_id IS NOT NULL) ON VIOLATION FAIL UPDATE -- fail
) AS
SELECT customer_id, SUM(amount) AS total
FROM orders
GROUP BY customer_id;
```

- `CREATE OR REFRESH STREAMING TABLE` = incremental (needs `STREAM`); `MATERIALIZED VIEW` = batch, recomputed (no `STREAM`).
- `STREAM read_files(...)` = Auto Loader; `STREAM(table)` = stream from another pipeline table.
- Expectations work on all three (streaming table from read_files, from STREAM(table), and materialized view) — but only inside an SDP pipeline.

##### **Expectations / constraints — `ON VIOLATION` actions**

| Syntax | Action on violation |
| --- | --- |
| `CONSTRAINT name EXPECT (cond)` | **Warn** — invalid record is **written**, but tracked in metrics |
| `CONSTRAINT name EXPECT (cond) ON VIOLATION DROP ROW` | **Drop** — invalid record **discarded** before writing |
| `CONSTRAINT name EXPECT (cond) ON VIOLATION FAIL UPDATE` | **Fail** — **stops the whole pipeline** on an invalid record |

##### **Schema options inside `read_files(...) only`** — format `option => 'value'`
This can be used only with read_files and not sith stream(table) or materialized view

| Option | What it does / values | Default if omitted |
| --- | --- | --- |
| `schema => '...'` | Full schema hardcoded — disables inference entirely | inference on (schema inferred) |
| `schemaHints => '...'` | Force types for specific columns, rest inferred (e.g. `'user_id BIGINT, created_at TIMESTAMP'`) | no hints — all inferred |
| `inferColumnTypes => true` | Infer column **types** too (not everything as string) | `false` |
| `rescuedDataColumn => '...'` | Column name for data that doesn't fit the schema | `_rescued_data` |
| `schemaEvolutionMode => '...'` | Behaviour on a **new column**:<br>`addNewColumns` — stream fails with `UnknownFieldException`, adds the new column on restart<br>`rescue` — new column not added to schema, data goes to `_rescued_data`, stream doesn't fail<br>`failOnNewColumns` — stream fails, must fix schema manually<br>`none` — new columns ignored, nothing added or rescued | `addNewColumns` |
| `schemaLocation => '...'` | Where the inferred schema is stored | managed automatically by SDP |

##### **Full reference — everything usable on a streaming table**

```sql
CREATE OR REFRESH STREAMING TABLE bronze_orders(
  -- column properties
  order_id      BIGINT NOT NULL COMMENT 'unique order id',
  customer_id   BIGINT,
  region        STRING,
  amount        DOUBLE DEFAULT 0.0,
  order_date    TIMESTAMP,
  row_id        BIGINT GENERATED ALWAYS AS IDENTITY,
  ingested_at   TIMESTAMP GENERATED ALWAYS AS (current_timestamp()),
  ssn           STRING MASK mask_ssn,

  -- expectations (3 types)
  CONSTRAINT valid_id     EXPECT (order_id IS NOT NULL),                           -- warn
  CONSTRAINT valid_amount EXPECT (amount >= 0)            ON VIOLATION DROP ROW,    -- drop
  CONSTRAINT valid_date   EXPECT (order_date IS NOT NULL) ON VIOLATION FAIL UPDATE, -- fail

  -- table constraints (informational, Unity Catalog only)
  CONSTRAINT pk PRIMARY KEY (order_id),
  CONSTRAINT fk FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
-- table clauses
COMMENT 'Raw orders ingested from landing zone'
TBLPROPERTIES ('quality' = 'bronze', 'pipelines.channel' = 'CURRENT')
CLUSTER BY (customer_id)                 -- or: CLUSTER BY AUTO / PARTITIONED BY (region)
DEFAULT COLLATION UTF8_BINARY
SCHEDULE EVERY 1 HOUR                     -- or: TRIGGER ON UPDATE AT MOST EVERY 5 MINUTES
WITH ROW FILTER my_filter_fn ON (region)
AS
SELECT *
FROM STREAM read_files(
  '/path/to/landing',
  format              => 'json',
  schemaHints         => 'order_id BIGINT, order_date TIMESTAMP',
  schemaEvolutionMode => 'addNewColumns',
  rescuedDataColumn   => '_rescued_data',
  inferColumnTypes    => true
);
```

**Column properties** (per column, inside the `( )`)

| Property | What it does |
| --- | --- |
| `NOT NULL` | Column can't be null. |
| `COMMENT 'text'` | Column description. |
| `DEFAULT expr` | Default value when none supplied. |
| `GENERATED ALWAYS AS (expr)` | Computed column from an expression (e.g. `current_timestamp()`). |
| `GENERATED ALWAYS AS IDENTITY` | Auto-increment column. |
| `MASK fn` | Column masking — applies a masking function (sensitive data). |

**Expectations** (data quality — inside the `( )`)

| Syntax | Action on violation |
| --- | --- |
| `CONSTRAINT n EXPECT (cond)` | **Warn** — invalid record written, tracked in metrics. |
| `CONSTRAINT n EXPECT (cond) ON VIOLATION DROP ROW` | **Drop** — invalid record discarded before writing. |
| `CONSTRAINT n EXPECT (cond) ON VIOLATION FAIL UPDATE` | **Fail** — stops the whole pipeline. |

**Table constraints** (informational only, Unity Catalog pipeline required)

| Constraint | What it does |
| --- | --- |
| `PRIMARY KEY (col)` | Informational primary key (not enforced, for lineage/tools). |
| `FOREIGN KEY (col) REFERENCES t(col)` | Informational foreign key. |

**Table clauses** (after the `)`, before `AS`)

| Clause | What it does |
| --- | --- |
| `COMMENT 'text'` | Table description (shown in Catalog Explorer). |
| `TBLPROPERTIES ('k'='v')` | User-defined properties / metadata (e.g. `pipelines.channel` = `CURRENT`/`PREVIEW`). |
| `CLUSTER BY (col, ...)` | Liquid clustering on chosen columns. Recommended over `PARTITIONED BY` for streaming tables. |
| `CLUSTER BY AUTO` | Automatic liquid clustering — Databricks picks the keys. |
| `PARTITIONED BY (col, ...)` | Partition by columns. **Mutually exclusive with `CLUSTER BY`.** |
| `DEFAULT COLLATION UTF8_BINARY` | Forces default collation (mandatory if the schema's collation isn't UTF8_BINARY). |
| `SCHEDULE EVERY n HOUR/DAY/...` / `SCHEDULE CRON '...'` | Refresh schedule for the table. |
| `TRIGGER ON UPDATE AT MOST EVERY ...` | Alternative to SCHEDULE — refresh on update, rate-limited (min 1 min). |
| `WITH ROW FILTER fn ON (col)` | Row-level security filter function. |

<br>

##### **`CREATE FLOW`** — separate the target table from the flow(s) that write into it

Normally a streaming table defines the table and its source together. `CREATE FLOW` splits them: define an empty target table, then one or more flows that write into it. Main use case: **multiple sources into one streaming table (fan-in)** — a normal `CREATE STREAMING TABLE ... AS SELECT` has only one source.

```sql
-- 1. target table (no source)
CREATE OR REFRESH STREAMING TABLE all_orders;

-- 2. multiple flows writing into it
CREATE FLOW orders_eu AS
INSERT INTO all_orders BY NAME
SELECT * FROM STREAM read_files('/eu/orders', format => 'json');

CREATE FLOW orders_us AS
INSERT INTO all_orders BY NAME
SELECT * FROM STREAM read_files('/us/orders', format => 'json');
```

- `INSERT INTO <table> BY NAME` — `BY NAME` maps columns by name (not position), safer.
- Each flow has its own name → tracked separately.
- Use for fan-in / union of streams into one table, or appending from different pipeline branches.
<br><br>


#### **`Python`**

##### **Full reference — everything usable on a streaming table (Python)**

```python
from pyspark import pipelines as dp
from pyspark.sql.functions import col

@dp.table(
    name="my_catalog.schema.orders",
    comment="Raw orders ingested from landing zone",
    table_properties={"quality": "bronze", "pipelines.channel": "CURRENT"},
    cluster_by=["customer_id"],           # or partition_cols=["region"] (mutually exclusive)
    schema="""
        order_id BIGINT NOT NULL COMMENT 'unique order id',
        customer_id BIGINT,
        region STRING,
        amount DOUBLE,
        order_date TIMESTAMP
    """
)
# expectations (3 types)
@dp.expect("valid_id", "order_id IS NOT NULL")                    # warn
@dp.expect_or_drop("valid_amount", "amount >= 0")                # drop
@dp.expect_or_fail("valid_date", "order_date IS NOT NULL")       # fail
def bronze_orders():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaHints", "order_id BIGINT, order_date TIMESTAMP")
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .option("cloudFiles.rescuedDataColumn", "_rescued_data")
        .option("cloudFiles.inferColumnTypes", "true")
        .load("/path/to/landing")
    )
```

**SQL → Python mapping**

| SQL | Python |
| --- | --- |
| `CREATE OR REFRESH STREAMING TABLE` | `@dp.table` |
| `CREATE OR REFRESH MATERIALIZED VIEW` | `@dp.materialized_view` |
| `COMMENT 'text'` (table) | `comment="text"` in decorator |
| `TBLPROPERTIES (...)` | `table_properties={...}` |
| `CLUSTER BY (col)` | `cluster_by=["col"]` |
| `PARTITIONED BY (col)` | `partition_cols=["col"]` |
| `STREAM read_files(...)` | `spark.readStream.format("cloudFiles")` |
| `STREAM(table)` | `spark.readStream.table("table")` |
| batch source | `spark.read.table("table")` |
| `schemaHints => '...'` | `.option("cloudFiles.schemaHints", "...")` |
| `schemaEvolutionMode => '...'` | `.option("cloudFiles.schemaEvolutionMode", "...")` |
| `rescuedDataColumn => '...'` | `.option("cloudFiles.rescuedDataColumn", "...")` |
| `inferColumnTypes => true` | `.option("cloudFiles.inferColumnTypes", "true")` |

**Expectations — decorator per action**

| SQL | Python (single) | Python (multiple) | Action |
| --- | --- | --- | --- |
| `EXPECT (cond)` | `@dp.expect("n", "cond")` | `@dp.expect_all({`<br>&nbsp;&nbsp;`"valid_amount": "amount >= 0",`<br>&nbsp;&nbsp;`"valid_id": "id IS NOT NULL",`<br>&nbsp;&nbsp;`"valid_date": "order_date IS NOT NULL"`<br>`})` | **Warn** |
| `EXPECT (cond) ON VIOLATION DROP ROW` | `@dp.expect_or_drop("n", "cond")` | `@dp.expect_all_or_drop({...})` | **Drop** |
| `EXPECT (cond) ON VIOLATION FAIL UPDATE` | `@dp.expect_or_fail("n", "cond")` | `@dp.expect_all_or_fail({...})` | **Fail** |

<br>

##### **`CREATE FLOW` (Python)** — multiple sources into one streaming table (fan-in)

```python
from pyspark import pipelines as dp

# 1. target table (no source)
dp.create_streaming_table("all_orders")

# 2. multiple flows writing into it
@dp.append_flow(target="all_orders")
def orders_eu():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/eu/orders")
    )

@dp.append_flow(target="all_orders")
def orders_us():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/us/orders")
    )
```

##### **Overview of `dp.methods`** 

**Dataset definition**

| Method | What it does |
| --- | --- |
| `@dp.table` | Streaming table (decorator over a function) |
| `@dp.materialized_view` | Materialized view |
| `@dp.temporary_view` | Temporary view (pipeline-scoped, doesn't persist) |

**Fan-in / flows**

| Method | What it does |
| --- | --- |
| `dp.create_streaming_table(...)` | Empty target table with no source (for fan-in) |
| `@dp.append_flow(target=...)` | Flow that writes into an existing streaming table |

**Expectations (data quality)**

| Method | Action |
| --- | --- |
| `@dp.expect("n","cond")` | Warn (single) |
| `@dp.expect_or_drop(...)` | Drop (single) |
| `@dp.expect_or_fail(...)` | Fail (single) |
| `@dp.expect_all({...})` | Warn (multiple at once) |
| `@dp.expect_all_or_drop({...})` | Drop (multiple at once) |
| `@dp.expect_all_or_fail({...})` | Fail (multiple at once) |

**CDC / SCD**

| Method | What it does |
| --- | --- |
| `dp.create_auto_cdc_flow(...)` | CDC / SCD Type 1/2 from a change feed |
| `dp.create_auto_cdc_from_snapshot_flow(...)` | CDC / SCD from snapshots (instead of a change feed) |

**External output**

| Method | What it does |
| --- | --- |
| `dp.create_sink(...)` | Write pipeline output to an external target (e.g. Kafka, or a Delta table outside the pipeline) |

<br><br>

### `Auto Loader`

Auto Loader incrementally ingests new files from cloud storage (S3 / ADLS / GCS) into Delta tables. It's a Structured Streaming source with format `cloudFiles`. It tracks already-processed files in the **checkpoint** (RocksDB key-value store), so it's idempotent — each file is processed once. Configured entirely through `cloudFiles.*` read options. Use it for recurring/continuous ingestion; use `COPY INTO` for one-shot batch backfills.

| Option | What it does |
| --- | --- |
| `cloudFiles.format` | The underlying file format: `json`, `csv`, `parquet`, `avro`, `text`, `binaryFile`. Required. |
| `cloudFiles.schemaLocation` | Directory where the inferred schema is stored and schema evolution is tracked. Enables schema inference/evolution. Can be the same dir as the checkpoint. |
| `cloudFiles.useNotifications` | `false` (default) = **directory listing** mode (periodically lists the source dir). `true` = **file notification** mode (subscribes to cloud notifications — SQS/SNS, Event Grid/Queue, Pub/Sub — scales to millions of files/hour, needs cloud permissions). Switching modes preserves the checkpoint's file tracking. |
| `cloudFiles.schemaEvolutionMode` | How Auto Loader reacts to new columns: `addNewColumns` (default when no schema given — adds new cols, stream fails then restarts with new schema), `rescue` (puts unexpected data in `_rescued_data`, never fails), `failOnNewColumns` (stream fails on new col until schema fixed), `none` (ignores new cols; default when a schema *is* provided). `addNewColumnsWithTypeWidening` (DBR 16.4+, Public Preview) also widens types like int→long. |
| `cloudFiles.inferColumnTypes` | `true` = infer actual types (int, timestamp...). `false` (default for most formats) = read everything as string. |
| `cloudFiles.schemaHints` | Manually fix the type of specific columns while letting the rest be inferred. Used *instead of* a full schema (schema + `addNewColumns` isn't allowed — use hints). |
| `cloudFiles.maxFilesPerTrigger` | Max number of new files processed per micro-batch (rate limit). Default 1000. |
| `cloudFiles.maxBytesPerTrigger` | Max amount of data per micro-batch (e.g. `10g`). Soft limit. |
| `cloudFiles.includeExistingFiles` | `true` (default) = also process files already in the dir when the stream first starts. `false` = only files that arrive after start. Only matters on first run. |
| `cloudFiles.allowOverwrites` | `true` = reprocess a file if it's modified/overwritten. `false` (default since DBR 17.3 LTS) = each filename processed once even if changed. |
| `cloudFiles.partitionColumns` | Hive-style partition columns to infer from the directory structure (e.g. `date=2025-01-01/`). |
| `cloudFiles.backfillInterval` | Triggers an async backfill on a schedule (e.g. `1 day`) to guarantee eventual completeness — safety net for notification mode where a cloud event could be missed. |
| `cloudFiles.cleanSource` | (DBR 16.4+) Archives processed files: `MOVE` (to another dir), `DELETE`, or `OFF` (default). |
| `rescuedDataColumn` | Name of the column collecting data that didn't match the schema (default `_rescued_data`). Always present unless disabled. Nothing is silently dropped. |
| `pathGlobfilter` | Only ingest files matching a glob pattern on the name (e.g. `*.png`, `*.json`). Filters *which* files to take — independent of `cloudFiles.format`, which decides *how* to parse them. |

**PySpark**

```python
df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/cat/sch/vol/_schema")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.maxFilesPerTrigger", 500)
    .load("/Volumes/cat/sch/vol/raw/"))

(df.writeStream
    .option("checkpointLocation", "/Volumes/cat/sch/vol/_checkpoint")
    .trigger(availableNow=True)        # process all available files then stop
    .toTable("cat.sch.bronze_events"))
```

**Spark SQL — `read_files()`**

`read_files()` is the SQL-native way to use Auto Loader. With the `STREAM` keyword inside a streaming table it runs Auto Loader under the hood. Streaming form only works inside Lakeflow Declarative Pipelines (DLT).

```sql
-- Streaming (Auto Loader) inside a DLT pipeline
CREATE OR REFRESH STREAMING TABLE bronze_events
AS SELECT *
FROM STREAM read_files(
  '/Volumes/cat/sch/vol/raw/',
  format => 'json',
  schemaEvolutionMode => 'addNewColumns'
);

-- Batch one-off read (no STREAM = plain read, not Auto Loader)
SELECT * FROM read_files('/Volumes/cat/sch/vol/raw/', format => 'json');
```

- **Idempotency lives in the checkpoint, not the discovery mode.** The mode is *how it finds* files; the checkpoint is *what it remembers*. You can switch listing ↔ notification without reprocessing.
- **`schemaLocation` vs `checkpointLocation`:** schemaLocation stores the inferred/evolving schema; checkpointLocation stores stream progress + processed-file state. Can point at the same dir. In DLT both are managed automatically.
- **Schema evolution restarts the stream:** with `addNewColumns`, when a new column appears the stream *fails once*, updates the stored schema, then a job restart picks it up. Configure the job to auto-restart.
- **`_rescued_data`** captures anything that doesn't fit the schema (extra columns, type mismatches) so nothing is lost. Drop it with `schemaEvolutionMode => 'none'`.
- **Trigger modes:** `availableNow=True` = batch-like, process everything currently available then stop (great for scheduled jobs). `processingTime="5 seconds"` = continuous micro-batches. Without a trigger it runs continuously by default.
- **Managed file events (2025 GA):** newer notification mode where Databricks provisions/operates the queues on top of Unity Catalog external locations — removes the manual IAM/permission setup of classic `useNotifications`. Recommended for new pipelines.

<br><br>

### `Delta Sharing`

Open protocol for sharing live data without copying. Recipient reads in place, read-only. Databricks-originated but open — recipient doesn't need Databricks. Two provider setups:

| | Provider off Databricks (open) | Provider on Databricks (D2D) |
| --- | --- | --- |
| What you exchange | Provider sends you a config/profile file (token + endpoint) | You send provider your sharing identifier (`CURRENT_METASTORE()`) |
| How recipient is created | `CREATE RECIPIENT x` → activation link → token | `CREATE RECIPIENT x USING ID '<your-metastore-id>'` |
| How you read | `delta_sharing` / `.format("deltaSharing")` + profile file | share appears in UC → `CREATE CATALOG ... USING SHARE` → plain `SELECT` |
| Token? | Yes, bearer token | No, identity via metastore ID |

<br>

#### <mark style="background-color: #FFF3CD">Provider setup (D2D / Unity Catalog)</mark>

Order: **SHARE → ADD TABLE → RECIPIENT → GRANT.** These are UC governance commands, not DataFrame API — Python just wraps the same SQL.

**SQL**

```sql
CREATE SHARE my_share;                                    -- 1. container
ALTER SHARE my_share ADD TABLE main.sales.transactions;   -- 2. add specific table
CREATE RECIPIENT acme_partner;                            -- 3. who (add USING ID '<metastore-id>' for D2D)
GRANT SELECT ON SHARE my_share TO RECIPIENT acme_partner; -- 4. grant
```

**Python** — wrap the same SQL in `spark.sql()`:

```python
spark.sql("CREATE SHARE my_share")
spark.sql("ALTER SHARE my_share ADD TABLE main.sales.transactions")
spark.sql("CREATE RECIPIENT acme_partner")
spark.sql("GRANT SELECT ON SHARE my_share TO RECIPIENT acme_partner")
```

Revoke: `REVOKE` / `DROP RECIPIENT` / `ALTER SHARE ... REMOVE TABLE`.

<br>

#### <mark style="background-color: #FFF3CD">Provider setup (off Databricks / open-source server)</mark>

No SQL — the provider runs an open-source Delta Sharing server and defines everything in `config.yaml`. Same `share → schema → table` hierarchy, expressed as YAML. The server is the gatekeeper; `location` points at the Delta table in cloud storage.

```yaml
version: 1
shares:
  - name: "share1"
    schemas:
      - name: "default"
        tables:
          - name: "cars"
            location: "s3a://my-bucket/cars"        # path to the Delta table
authorization:
  bearerToken: "my-secret-token"                    # token the recipient must send
host: "localhost"
port: 9999
endpoint: "/delta-sharing"
```

The recipient then gets a **profile file** (`.share`) — endpoint + token — and reads with it:

```json
{
  "shareCredentialsVersion": 1,
  "endpoint": "https://sharing.example.com/delta-sharing",
  "bearerToken": "my-secret-token"
}
```

The recipient then reads table as

```python
df = (spark.read
    .format("deltaSharing")
    .load("/path/to/config.share#share1.default.cars"))
```

<br><br>

### `Query Federation (Lakehouse Federation)`

Query data in **external databases** (PostgreSQL, MySQL, Snowflake, Redshift, SQL Server, BigQuery...) directly from Databricks — **without copying/ingesting it first**. The data stays in the source; you query it remotely as if it were a Unity Catalog table.

**Setup — 3 steps:**

```sql
-- 1. connection to the external DB
CREATE CONNECTION my_pg TYPE postgresql
OPTIONS (host '...', port '5432', user '...', password '...');

-- 2. foreign catalog = mirror of that DB in Unity Catalog
CREATE FOREIGN CATALOG pg_catalog USING CONNECTION my_pg
OPTIONS (database 'sales_db');

-- 3. query it like a normal table
SELECT * FROM pg_catalog.public.customers;
```

**Key points:**
- **No data copying** — you query the source directly, data stays where it is.
- **Query pushdown** — Databricks pushes filters/aggregations into the source DB to minimize data transferred over the network.
- **Unity Catalog governance** applies — same permissions, lineage as native tables.
- **Read-only** (primarily) — for reading/analysis, not writing back to the source.
- Good for: quick exploration, joining external data with Databricks tables, avoiding duplication. Not for: heavy repeated production workloads on big data (loads the source DB, slower than native Delta).

**Don't confuse with Delta Sharing:**
- **Delta Sharing** = someone shares *their* Delta data *to you* via an open protocol (provider → recipient).
- **Query Federation** = *you* connect *out* to a foreign (non-Databricks) database and query it remotely.

<br><br>

### `Pipeline execution modes (Lakeflow Declarative Pipelines)`

Two independent settings combine — one from each axis:
- **Development vs Production** = how the pipeline behaves (cluster lifecycle + retries).
- **Triggered vs Continuous** = how long/often it runs.

| Setting | What it does |
| --- | --- |
| **Development** | Cluster is **reused** (not torn down) for fast iteration; **no automatic retries** on failure (see errors immediately). For building/debugging. |
| **Production** | Cluster is **terminated** after the run (saves cost); **retry logic** applied on failure (resilient). For real runs. |
| **Triggered** | Runs once, processes currently available data, then **stops**. Batch-like — for scheduled runs. |
| **Continuous** | Runs **non-stop**, processing data as it arrives (real-time / near-real-time). |

**The 4 combinations:**

| Combination | What it means in practice |
| --- | --- |
| **Development + Triggered** | Building/debugging a batch pipeline. Cluster stays warm between runs, no retries, processes available data then stops. Fastest iteration loop. |
| **Development + Continuous** | Building/debugging a streaming pipeline. Runs non-stop with a reused cluster and no retries — you watch it process live data and see failures instantly. |
| **Production + Triggered** | Scheduled batch job in prod. Spins up a cluster, processes available data, tears the cluster down, retries on failure. Cost-efficient scheduled ingestion. |
| **Production + Continuous** | Always-on streaming job in prod. Runs continuously with retry logic; cluster stays up because the pipeline never stops. Real-time production processing. |

Note: Dev/Prod and Triggered/Continuous are **separate axes** — any of the 4 combinations is valid.

## Spark SQL

<br>

| Command | What it does |
| --- | --- |
| `INSERT INTO <table_name> SELECT ...` | Appends the query result to the table — existing rows stay. |
| `INSERT OVERWRITE <table_name> SELECT ...` | Replaces the **entire** contents of the table with the query result — old rows gone. |
| `TRUNCATE TABLE <table_name>` | Deletes all rows but keeps the table and its schema (empties it). |
| `UPDATE <table_name> SET col = val WHERE ...` | Changes values in existing rows matching the `WHERE` condition. |
| `ALTER TABLE <table_name> RENAME COLUMN old TO new` | Renames a column. **Delta only, requires column mapping enabled.** Metadata-only — no data rewrite (so it's cheap even on huge tables).<br>Enable first: `ALTER TABLE <table_name> SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name')`<br>Without column mapping the command fails — parquet can't rename a column in place without rewriting files.<br>Don't fake it with `UPDATE <table_name> SET new_col = old_col` — that rewrites all rows and leaves you with a duplicate column instead of a rename. |
| `ALTER TABLE` | `RENAME TO new_name` — renames the table.<br>`ADD COLUMN c TYPE` — adds a column (existing rows get NULL; no DEFAULT at add-time on Delta).<br>`DROP COLUMN c` — drops a column (Delta: needs column mapping).<br>`RENAME COLUMN old TO new` — renames a column (Delta: needs column mapping; metadata-only).<br>`ALTER COLUMN c ...` — changes a column: `SET/DROP NOT NULL`, `TYPE`, `SET DEFAULT`, `COMMENT`, `FIRST/AFTER`.<br>`SET TBLPROPERTIES (k = v)` — sets table config (column mapping, CDF, deletion vectors...).<br>`UNSET TBLPROPERTIES (k)` — removes a table property.<br>`ADD/DROP CONSTRAINT ...` — adds/drops constraints (CHECK, PK, FK).<br>`ADD/DROP PARTITION ...` — manages partitions.<br>`CLUSTER BY (cols)` — sets/changes liquid clustering columns.<br>`SET LOCATION ...` — points the table at a different storage path.<br>`SET OWNER TO principal` — changes table ownership (UC). |
| `COMMENT ON TABLE <table_name> IS 'comment'` | Adds/updates a comment on an **existing** table. |
| `CREATE TABLE <table_name> ... COMMENT 'comment'` | Sets a comment **at creation time**.
| `ALTER TABLE <table_name> SET TBLPROPERTIES ('comment' = 'comment')` | Alternative way to set a table comment via table properties. |
| `COMMENT ON COLUMN <table_name>.col IS 'comment'` | Adds/updates a comment on a specific **column**. |



<br><br>

## PySpark
<br>

| Command | What it does |
| --- | --- |
| `create_map(*cols)` | Builds a map (key-value) column from alternating key, value columns. E.g. `df.withColumn("m", create_map(lit("a"), col("x"), lit("b"), col("y")))` → map `{a: x, b: y}`. Needs `from pyspark.sql.functions import create_map, lit, col`. |

<br><br>

## Databricks-specific vs open-source Spark

| Feature | Databricks or Spark? | Note |
| --- | --- | --- |
| Structured Streaming | Spark | Native streaming engine. Auto Loader is built on top of it. |
| Auto Loader (`cloudFiles`) | Databricks | The `cloudFiles` source + notification mode, `_rescued_data`, RocksDB file tracking. Not in open-source Spark. |
| `read_files()` | Databricks | SQL-native wrapper; uses Auto Loader when streaming. |
| Delta Sharing | Databricks-originated, **open** | Open protocol for sharing live Delta data without copying. Donated to Linux Foundation — recipient doesn't need Databricks. |
| Query Federation (Lakehouse Federation) | Databricks | Query external DBs (Postgres, Snowflake, MySQL...) in place via UC foreign catalogs. Not in open-source Spark. |

<br><br><br>

# 🟡 Additional Information on Databricks Platform
<br>

## Debugging
<br>

**Key split: is the job HANGING (no error) or did it CRASH (exception)?** Different problems, different tools.

| Tool | When to use it |
| --- | --- |
| **Spark UI → thread dump** | Job is **hanging** — stuck, no progress, **no error**. Takes a snapshot of all JVM driver/executor thread states, showing which threads are blocked/waiting and on what. Answers *"why is it stuck doing nothing?"* |
| **Executor / driver logs** | Job **crashed** with an exception. Most detailed view — captures the full traceback from the executor side, including which data/types caused the failure. Tedious to dig through, but the most complete. Answers *"why did it fail?"* |
| **`%debug`** | **Post-mortem** after an exception — drops you into the state at the moment of failure. Returns the driver-side (consolidated) traceback the driver got back from the nodes. Partial for distributed code (UDFs) — shows the exception, not the full executor context. |
| **Interactive Debugger** | **Live** debugging — step through code line by line, inspect variables as they change (like stepping through an Excel formula). Needs breakpoints set beforehand. **Driver-side only** — can't see into executors, so useless for a hang or for distributed UDF errors. |

<br><br>

## Optimization
<br>

### Predicate pushdown

Filters (`WHERE`) get "pushed down" to the file read — Spark uses Parquet min/max stats to skip row-groups that don't match, instead of reading everything and filtering after. Mostly automatic; you enable it by writing good SQL:
- Filter early (put `WHERE` before joins/aggregations).
- Filter on raw columns — `WHERE region = 'EU'` pushes down; `WHERE UPPER(region) = 'EU'` usually breaks it (a function around the column kills pushdown).

<br><br>

### Column pruning

Parquet is columnar, so Spark reads only the columns you actually ask for — **if you name them**. `SELECT *` forces it to read every column.
- `SELECT region, amount FROM sales` → reads 2 columns.
- `SELECT * FROM sales` → reads all columns. Avoid when you don't need them.

<br><br>

### Partitioning

`PARTITIONED BY (col)` at write time stores data in separate folders per value. A `WHERE` on the partition column skips whole folders without reading them (partition pruning).
- Best for low-cardinality columns (e.g. `date`, `country`).
- Too many small partitions on a high-cardinality column hurts — that's where liquid clustering wins instead.

<br><br>

### Liquid clustering

`CLUSTER BY (col)` — modern replacement for partitioning + ZORDER. Physically co-locates data by the clustering key, so file skipping works even on high-cardinality columns. Incremental: `OPTIMIZE` only reclusters newly-written data, so it stays cheap.
- Not compatible with partitioning or ZORDER (use one approach).
- `OPTIMIZE FULL` forces a full recluster — needed after first enabling clustering or changing clustering keys.

<br><br>

### OPTIMIZE

Compacts many small files into fewer, larger, evenly-sized files and improves min/max stats (which makes skipping/pushdown more effective). On liquid-clustered tables it also reclusters.
- Incremental on clustered tables — most runs are quick; a re-run with no new data is a no-op.
- Solves the "small files problem" (lots of tiny files = slow scans).

<br><br>

### OPTIMIZE: partitioning vs liquid clustering

`OPTIMIZE` does more on a clustered table. With partitioning it only compacts small files (ordering is handled by the folders). With liquid clustering there are no folders, so `OPTIMIZE` also physically reorders rows by the clustering key.

| | Partitioning + OPTIMIZE | Liquid clustering + OPTIMIZE |
| --- | --- | --- |
| Bin-packing (compacts small files) | Yes | Yes |
| Reclustering (reorders rows by key) | No | Yes |
| Where it happens | Within each partition folder | Across the whole table (no folders) |

- **Bin-packing** = merges many small files into fewer, evenly-sized ones (fixes the small-files problem).
- **Reclustering** = rearranges rows so similar key values sit together, updating each file's min/max stats for data skipping.
- On clustered tables reclustering is **incremental** — only newly-written data is reorganized, so most runs are quick and a re-run with no new data is a no-op.
  
<br><br>

### VACUUM

Deletes old data files no longer referenced by the Delta table (leftovers from updates/deletes/OPTIMIZE) past a retention period (default 7 days). Frees storage.
- Doesn't speed up queries directly — it's cleanup, not layout optimization.
- Removes the ability to time-travel to versions older than what you vacuumed. Don't set retention too low.

<br><br>