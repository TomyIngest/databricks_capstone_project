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