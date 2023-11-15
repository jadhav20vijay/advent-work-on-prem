# Databricks notebook source
# test link to the file

# input_path = "abfss://bronze@onpremsqlsa.dfs.core.windows.net/SalesLT/Address/Address.parquet"




# COMMAND ----------

# df = spark.read.format('parquet').load(input_path)

# COMMAND ----------

# display(df)

# COMMAND ----------



# COMMAND ----------

all_tables = []

# COMMAND ----------

tables = dbutils.fs.ls("abfss://bronze@onpremsqlsa.dfs.core.windows.net/SalesLT/")
for i in tables:
    all_tables.append(i.name.split('/')[0])

# COMMAND ----------

from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType

for i in all_tables:
    file_name = "abfss://bronze@onpremsqlsa.dfs.core.windows.net/SalesLT/"+ i +"/" +i+ ".parquet"
    df = spark.read.format('parquet').load(file_name)
    for col in df.columns:
        if "Date" in col or "date" in col:
            df = df.withColumn(col, date_format(from_utc_timestamp(df[col].cast(TimestampType()), "UTC"), "yyyy-MM-dd"))
    output_path = 'abfss://silver@onpremsqlsa.dfs.core.windows.net/SalesLT/' + i + '/'
    df.write.format('delta').mode('overwrite').save(output_path)

# COMMAND ----------

display(df)
