from databricks.connect import DatabricksSession
spark = DatabricksSession.builder.profile("Data_Engineering_001").serverless(True).getOrCreate()

spark.sql("SELECT 'Running pyspark code' ").show()







