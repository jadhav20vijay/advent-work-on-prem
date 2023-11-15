# Databricks notebook source
# test link to the file

# input_path = 'abfss://silver@onpremsqlsa.dfs.core.windows.net/SalesLT/Address/'

# COMMAND ----------

# df = spark.read.format('delta').load(input_path)

# COMMAND ----------

# display(df)

# COMMAND ----------

table_list = []
for i in  dbutils.fs.ls ('abfss://silver@onpremsqlsa.dfs.core.windows.net/SalesLT'):
    table_list.append(i.name.split('/')[0])

# COMMAND ----------

table_list

# COMMAND ----------


for table in table_list:
    path = ('abfss://silver@onpremsqlsa.dfs.core.windows.net/SalesLT/' + table)
    print(path)
    df = spark.read.format('delta').load(path)
    column_names = df.columns
    for old_column in column_names:
        new_column = "".join(["_" + char if char.isupper() and not old_column[i - 1].isupper() else char for i, char in enumerate(old_column)]).lstrip("_")
        df = df.withColumnRenamed(old_column, new_column)
        output_path = ('abfss://gold@onpremsqlsa.dfs.core.windows.net/SalesLT/' + table + '/')
        df.write.format('delta').mode('overwrite').option("overwriteSchema", "true").save(output_path)



# COMMAND ----------

display(df)
