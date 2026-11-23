- [🟡 Databricks fundamentals ](#-databricks-fundamentals-)
  - [dbutils – file system](#dbutils--file-system)
- [🟡 Data Ingestion ](#-data-ingestion-)
  - [CTAS](#ctas)
  - [COPY INTO](#copy-into)
  - [Auto Loader](#auto-loader)
  - [SDP (Spark Declarative Pipelines)](#sdp-spark-declarative-pipelines)

<br><br>

# 🟡 Databricks fundamentals <br>

<br>

## dbutils – file system

| Command | What it does |
| --- | --- |
| `dbutils.fs.ls(path)` | Lists the content of a folder: files and subfolders. Returns a list of `FileInfo` objects (`path`, `name`, `size`, `modificationTime`). Folder names end with `/`. Wrap it in `display()` to see the result as a table, e.g. `display(dbutils.fs.ls("/Volumes/main/bronze/raw/"))`. |
| `dbutils.fs.cp(src, dst, recurse=True)` | Copies a file or a whole folder from `src` to `dst`. A single file needs no `recurse`. A folder needs `recurse=True` to copy everything inside it. The source stays where it was. E.g. `dbutils.fs.cp("/Volumes/main/bronze/raw/orders.csv", "/Volumes/main/bronze/archive/orders.csv")`. |
| `dbutils.fs.mv(src, dst, recurse=True)` | Moves a file or a whole folder from `src` to `dst`. Same as `cp`, but the source is deleted afterwards. Use `recurse=True` for folders. Handy for moving processed files from a landing folder to an archive. |
| `dbutils.fs.rm(path, recurse=True)` | Deletes a file or a folder. A folder with content needs `recurse=True`, otherwise the command fails. ⚠️ There is no recycle bin, so deleted files are gone for good. |
| `dbutils.fs.mkdirs(path)` | Creates a folder, including any missing parent folders on the way (like `mkdir -p`). If the folder already exists, nothing happens and there's no error. E.g. `dbutils.fs.mkdirs("/Volumes/main/bronze/raw/2026/11/")`. |

<br><br>

# 🟡 Data Ingestion <br>

<br>

## CTAS

🔶 **Databricks-specific:** all SQL versions (they use `read_files()`) · 🟢 **Open source (Apache Spark):** PySpark version

| Command | What it does |
| --- | --- |
| <pre><span style="color:#569CD6">CREATE TABLE</span> new_table <span style="color:#569CD6">AS</span><br><span style="color:#569CD6">SELECT</span> *<br><span style="color:#569CD6">FROM</span> <span style="color:#C586C0">read_files</span>(<br>  <span style="color:#6A9955">&lt;path_to_file(s)&gt;</span>,<br>  format =&gt; <span style="color:#CE9178">'&lt;file_type&gt;'</span>,<br>  <span style="color:#6A9955">&lt;other_format_specific_options&gt;</span><br>);</pre> | **Basic CTAS.** Creates a Delta table from the query result, the schema is inferred from the files. One-time batch load, fails if the table already exists. |
| <pre><span style="color:#569CD6">CREATE TABLE</span> main.bronze.orders <span style="color:#569CD6">AS</span><br><span style="color:#569CD6">SELECT</span> *<br><span style="color:#569CD6">FROM</span> <span style="color:#C586C0">read_files</span>(<br>  <span style="color:#CE9178">'/Volumes/main/bronze/raw/orders/'</span>,<br>  format =&gt; <span style="color:#CE9178">'csv'</span>,<br>  header =&gt; <span style="color:#569CD6">true</span>,<br>  schema =&gt; <span style="color:#CE9178">'order_id INT, customer STRING, amount DECIMAL(10,2)'</span><br>);</pre> | **Full schema.** You set the types of all columns, nothing is inferred. CTAS has no column list (`CREATE TABLE t (id INT…) AS` doesn't work), so the schema goes into `read_files`. |
| <pre><span style="color:#569CD6">CREATE TABLE</span> main.bronze.orders <span style="color:#569CD6">AS</span><br><span style="color:#569CD6">SELECT</span> *<br><span style="color:#569CD6">FROM</span> <span style="color:#C586C0">read_files</span>(<br>  <span style="color:#CE9178">'/Volumes/main/bronze/raw/orders/'</span>,<br>  format =&gt; <span style="color:#CE9178">'csv'</span>,<br>  header =&gt; <span style="color:#569CD6">true</span>,<br>  schemaHints =&gt; <span style="color:#CE9178">'amount DECIMAL(10,2)'</span><br>);</pre> | **Schema hints.** The schema is inferred, only the listed columns get the type you set. |
| <pre><span style="color:#569CD6">CREATE TABLE</span> main.bronze.orders <span style="color:#569CD6">AS</span><br><span style="color:#569CD6">SELECT</span><br>  <span style="color:#C586C0">CAST</span>(order_id <span style="color:#569CD6">AS INT</span>) <span style="color:#569CD6">AS</span> order_id,<br>  customer,<br>  <span style="color:#C586C0">CAST</span>(amount <span style="color:#569CD6">AS DECIMAL</span>(10,2)) <span style="color:#569CD6">AS</span> amount<br><span style="color:#569CD6">FROM</span> <span style="color:#C586C0">read_files</span>(<br>  <span style="color:#CE9178">'/Volumes/main/bronze/raw/orders/'</span>,<br>  format =&gt; <span style="color:#CE9178">'csv'</span>,<br>  header =&gt; <span style="color:#569CD6">true</span><br>);</pre> | **CAST in SELECT.** Casts (and renames) columns after reading. The table gets exactly the columns from the `SELECT`. |
| <pre>df = (spark.read<br>        .<span style="color:#C586C0">format</span>(<span style="color:#CE9178">"csv"</span>)<br>        .<span style="color:#C586C0">option</span>(<span style="color:#CE9178">"header"</span>, <span style="color:#569CD6">True</span>)<br>        .<span style="color:#C586C0">option</span>(<span style="color:#CE9178">"inferSchema"</span>, <span style="color:#569CD6">True</span>)<br>        .<span style="color:#C586C0">load</span>(<span style="color:#CE9178">"/Volumes/main/bronze/raw/orders/"</span>))<br><br>df.write.<span style="color:#C586C0">saveAsTable</span>(<span style="color:#CE9178">"main.bronze.orders"</span>)</pre> | **PySpark.** There's no `read_files()`, so it's two steps: read into a DataFrame, then save as a table. Without `inferSchema`, all CSV columns are `STRING`. |

<br>

## COPY INTO

🔶 **Databricks only** (SQL only, no PySpark version)

| Command | What it does |
| --- | --- |
| <pre style="min-width:350px"><span style="color:#569CD6">CREATE TABLE</span> main.bronze.orders;<br><br><span style="color:#569CD6">COPY INTO</span> main.bronze.orders<br><span style="color:#569CD6">FROM</span> <span style="color:#CE9178">'/Volumes/main/bronze/raw/orders/'</span><br><span style="color:#569CD6">FILEFORMAT</span> = <span style="color:#569CD6">CSV</span><br><span style="color:#569CD6">FORMAT_OPTIONS</span> (<span style="color:#CE9178">'header'</span> = <span style="color:#CE9178">'true'</span>, <span style="color:#CE9178">'inferSchema'</span> = <span style="color:#CE9178">'true'</span>)<br><span style="color:#569CD6">COPY_OPTIONS</span> (<span style="color:#CE9178">'mergeSchema'</span> = <span style="color:#CE9178">'true'</span>)</pre> | **Basic COPY INTO.** Loads files from a folder into an existing table. It's **idempotent**: it remembers which files it already loaded and skips them on the next run, so only new files get added. The table can be created empty, without columns. `FORMAT_OPTIONS` are options for reading the files (e.g. `'header' = 'true'`), `COPY_OPTIONS` control the load itself (e.g. `'mergeSchema' = 'true'`). |

<br>

## Auto Loader

🔶 **Databricks only** (both Python and SQL: `cloudFiles` / `read_files()`)

| Command | What it does |
| --- | --- |
| <pre>(spark<br>  .readStream<br>    .<span style="color:#C586C0">format</span>(<span style="color:#CE9178">"cloudFiles"</span>)<br>    .<span style="color:#C586C0">option</span>(<span style="color:#CE9178">"cloudFiles.format"</span>, <span style="color:#CE9178">"json"</span>)<br>    .<span style="color:#C586C0">option</span>(<span style="color:#CE9178">"cloudFiles.schemaLocation"</span>, <span style="color:#CE9178">"/Volumes/main/bronze/checkpoints/events/"</span>)<br>    .<span style="color:#C586C0">load</span>(<span style="color:#CE9178">"/Volumes/main/bronze/raw/events/"</span>)<br>  .writeStream<br>    .<span style="color:#C586C0">option</span>(<span style="color:#CE9178">"checkpointLocation"</span>, <span style="color:#CE9178">"/Volumes/main/bronze/checkpoints/events/"</span>)<br>    .<span style="color:#C586C0">trigger</span>(processingTime=<span style="color:#CE9178">"5 seconds"</span>)<br>    <span style="color:#6A9955"># .trigger(availableNow=True)   # or: process all new files and stop</span><br>    .<span style="color:#C586C0">toTable</span>(<span style="color:#CE9178">"main.bronze.events"</span>)<br>)</pre> | **Python Auto Loader.** Incremental load with Structured Streaming: each run picks up only new files. `cloudFiles.schemaLocation` stores the inferred schema and its changes, `checkpointLocation` stores which files were already processed. `trigger(processingTime="5 seconds")` keeps the stream running and checks for new files every 5 s. `trigger(availableNow=True)` processes all new files and stops (incremental batch). |
| <pre><span style="color:#569CD6">CREATE OR REFRESH STREAMING TABLE</span><br>  main.bronze.events<br><span style="color:#569CD6">SCHEDULE EVERY</span> 1 <span style="color:#569CD6">HOUR</span><br><span style="color:#6A9955">-- TRIGGER ON UPDATE   -- or: refresh when new data arrives</span><br><span style="color:#569CD6">AS</span><br><span style="color:#569CD6">SELECT</span> *<br><span style="color:#569CD6">FROM STREAM</span> <span style="color:#C586C0">read_files</span>(<br>  <span style="color:#CE9178">'/Volumes/main/bronze/raw/events/'</span>,<br>  format =&gt; <span style="color:#CE9178">'json'</span><br>);<br><br><span style="color:#6A9955">-- REFRESH STREAMING TABLE main.bronze.events;   -- manual refresh</span></pre> | **Auto Loader with SQL (streaming table).** Run in Databricks SQL, no pipeline to manage. `STREAM read_files(...)` reads only new files. The checkpoint and schema location are managed for you. `CREATE OR REFRESH` creates the table or updates it, so a rerun doesn't fail. `SCHEDULE EVERY 1 HOUR` refreshes it on a schedule. |

<br>

## SDP (Spark Declarative Pipelines)

🔶 **Databricks-specific** in this form (`read_files`, Auto Loader, expectations) · 🟢 the core SDP framework is also open source in Apache Spark 4.1+

**SQL**

| Command | What it does |
| --- | --- |
| <pre><span style="color:#6A9955">-- BRONZE</span><br><span style="color:#569CD6">CREATE OR REFRESH STREAMING TABLE</span> bronze_events<br><span style="color:#569CD6">AS SELECT</span> *<br><span style="color:#569CD6">FROM STREAM</span> <span style="color:#C586C0">read_files</span>(<br>  <span style="color:#CE9178">'/Volumes/main/bronze/raw/events/'</span>,<br>  format =&gt; <span style="color:#CE9178">'json'</span><br>);<br><br><span style="color:#6A9955">-- SILVER</span><br><span style="color:#569CD6">CREATE OR REFRESH STREAMING TABLE</span> silver_events (<br>  <span style="color:#569CD6">CONSTRAINT</span> valid_id <span style="color:#569CD6">EXPECT</span> (event_id <span style="color:#569CD6">IS NOT NULL</span>) <span style="color:#569CD6">ON VIOLATION DROP ROW</span><br>)<br><span style="color:#569CD6">AS SELECT</span> *<br><span style="color:#569CD6">FROM STREAM</span> bronze_events;</pre> | **SDP in SQL.** You only declare the tables, the pipeline works out the order from the dependencies (silver reads from bronze). `STREAM read_files` is Auto Loader inside. `EXPECT ... ON VIOLATION DROP ROW` drops bad rows (all options: see the table below). Checkpoints and schema location are managed for you. Runs only as a pipeline, not as a notebook cell. |

🔶 Expectations in SQL work in SDP and in Databricks SQL streaming tables / materialized views.

| Format | What happens to a bad row |
| --- | --- |
| `CONSTRAINT name EXPECT (condition)` | **Warn** (default): the row is kept, the violation is only counted in the metrics. |
| `CONSTRAINT name EXPECT (condition) ON VIOLATION DROP ROW` | **Drop**: the row is not written, the count shows in the metrics. |
| `CONSTRAINT name EXPECT (condition) ON VIOLATION FAIL UPDATE` | **Fail**: the whole update stops, nothing is written. |

<br>

**Python**

| Command | What it does |
| --- | --- |
| <pre><span style="color:#569CD6">from</span> pyspark <span style="color:#569CD6">import</span> pipelines <span style="color:#569CD6">as</span> dp<br><br><span style="color:#6A9955"># BRONZE</span><br><span style="color:#C586C0">@dp.table</span>(name=<span style="color:#CE9178">"bronze_events"</span>)<br><span style="color:#569CD6">def</span> <span style="color:#C586C0">bronze_events</span>():<br>    <span style="color:#569CD6">return</span> (spark.readStream<br>              .<span style="color:#C586C0">format</span>(<span style="color:#CE9178">"cloudFiles"</span>)<br>              .<span style="color:#C586C0">option</span>(<span style="color:#CE9178">"cloudFiles.format"</span>, <span style="color:#CE9178">"json"</span>)<br>              .<span style="color:#C586C0">load</span>(<span style="color:#CE9178">"/Volumes/main/bronze/raw/events/"</span>))<br><br><span style="color:#6A9955"># SILVER</span><br><span style="color:#C586C0">@dp.table</span>(name=<span style="color:#CE9178">"silver_events"</span>)<br><span style="color:#C586C0">@dp.expect_or_drop</span>(<span style="color:#CE9178">"valid_id"</span>, <span style="color:#CE9178">"event_id IS NOT NULL"</span>)<br><span style="color:#569CD6">def</span> <span style="color:#C586C0">silver_events</span>():<br>    <span style="color:#569CD6">return</span> spark.readStream.<span style="color:#C586C0">table</span>(<span style="color:#CE9178">"bronze_events"</span>)</pre> | **SDP in Python.** Same as SQL, written with decorators. The function only returns a DataFrame: no `writeStream`, checkpoint or trigger. `@dp.expect_or_drop` is the same as `ON VIOLATION DROP ROW` (all options: see the table below). Older code uses `import dlt` / `@dlt.table`. |

🔶 Expectations in Python work only in SDP.

| Format | What happens to a bad row |
| --- | --- |
| `@dp.expect("name", "condition")` | **Warn**: kept, only counted. |
| `@dp.expect_or_drop("name", "condition")` | **Drop**: not written. |
| `@dp.expect_or_fail("name", "condition")` | **Fail**: the update stops. |
| `@dp.expect_all({"name1": "cond1", "name2": "cond2"})` | **Warn**, several rules at once (dict name → condition). |
| `@dp.expect_all_or_drop({...})` | **Drop** if any of the rules fails. |
| `@dp.expect_all_or_fail({...})` | **Fail** if any of the rules fails. |

<br>
