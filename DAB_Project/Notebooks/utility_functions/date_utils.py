
import pyspark.sql.functions as sf

def timestamp_to_date(df,time_column,date_column):
    return  df.withColumn(date_column, sf.to_date(sf.col(time_column)))





















