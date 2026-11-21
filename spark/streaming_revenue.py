# Lecture en mode streaming
from sqlite3 import SQLITE_CONSTRAINT_PRIMARYKEY

from narwhals import Schema

from pyspark.sql.functions import col, sum as spark_sum

stream_df = SQLITE_CONSTRAINT_PRIMARYKEY.readStream \
    .schema(Schema) \
    .option("header", True) \
    .csv("hdfs://namenode:8020/stream_input")

# Traitement : revenu par pays en temps réel
result = stream_df.filter(col("Quantity") > 0) \
    .withColumn("Revenue", col("Quantity") * col("UnitPrice")) \
    .groupBy("Country") \
    .agg(spark_sum("Revenue").alias("TotalRevenue"))

# Sortie console (pour la démo)
query = result.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()
