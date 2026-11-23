- [🟡 Spark SQL \& PySpark ](#-spark-sql--pyspark-)
  - [Catalog \& schema context](#catalog--schema-context)
  - [Exploring objects](#exploring-objects)

<br><br>

# 🟡 Spark SQL & PySpark <br>

<br>

## Catalog & schema context

| Task | Spark SQL | PySpark | What it does |
| --- | --- | --- | --- |
| **Set the default catalog** | `USE CATALOG my_catalog;` | `spark.catalog.setCurrentCatalog("my_catalog")` | Sets the catalog that is used when a name has no catalog in it. |
| **Set the default schema** | `USE SCHEMA data_ingestion;` | `spark.catalog.setCurrentDatabase("data_ingestion")` | Sets the schema inside the current catalog. Together with `USE CATALOG`, you can then write short table names: `orders` means `my_catalog.data_ingestion.orders`. Both settings last for the current Spark session (e.g. the notebook). PySpark still uses the old name **database** for a schema. Same thing, different word. |
| **Show the current catalog & schema** | `SELECT`<br>`  current_catalog(),`<br>`  current_schema();` | `spark.catalog.currentCatalog()`<br>`spark.catalog.currentDatabase()` | Shows which catalog and schema are set right now. Run it after `USE ...` to check, or when you're not sure where an unqualified table name points to. The SQL version returns a one-row table, the PySpark version returns plain strings. |

<br>

## Exploring objects

| Task | Spark SQL | PySpark | What it does |
| --- | --- | --- | --- |
| **List schemas** | `SHOW SCHEMAS;` | `spark.catalog.listDatabases()` | Lists all schemas in the current catalog. Handy for a quick look at what's in the catalog before `USE SCHEMA`. |
| **Describe a schema** | `DESCRIBE SCHEMA EXTENDED data_ingestion;` | `spark.catalog.getDatabase("data_ingestion")` | Shows details about a schema: catalog, name, comment, storage location and owner. `EXTENDED` adds the schema properties too. The PySpark version returns fewer details (name, catalog, description, location). |
| **Describe a table** | `DESCRIBE TABLE EXTENDED orders;` | `spark.catalog.getTable("orders")`<br>`spark.catalog.listColumns("orders")` | First lists the columns with their data types and comments. `EXTENDED` adds a **Detailed Table Information** part below: catalog, schema, owner, created time, type (`MANAGED` / `EXTERNAL`), storage location, format (e.g. `delta`) and table properties. In PySpark, `getTable()` returns the table info and `listColumns()` the columns. |
| **Describe a volume** | `DESCRIBE VOLUME my_volume;` | – | Shows details about a Unity Catalog volume: catalog, schema, name, owner, type (`MANAGED` / `EXTERNAL`), storage location and comment. There's no `EXTENDED` here and no PySpark API for it. In Python, use `spark.sql("DESCRIBE VOLUME my_volume")`. |

<br>
