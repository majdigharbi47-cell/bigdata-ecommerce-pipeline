from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, avg, countDistinct, when
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator
# Initialisation de la session Spark avec connexion HDFS
spark = SparkSession.builder \
.appName("RetailML") \
.config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020") \
.getOrCreate()
# Lecture du dataset depuis HDFS
df = spark.read.csv("hdfs://namenode:8020/retail_input/online_retail.csv",
header=True, inferSchema=True)
# Nettoyage et feature engineering
df_clean = df.filter(~col("InvoiceNo").startswith("C")) \
.filter(col("CustomerID").isNotNull()) \
.withColumn("Revenue", col("Quantity") * col("UnitPrice"))
# Agrégation par client (features)
customers = df_clean.groupBy("CustomerID").agg(
spark_sum("Revenue").alias("TotalRevenue"),
spark_sum("Quantity").alias("TotalQuantity"),
avg("UnitPrice").alias("AvgUnitPrice"),
countDistinct("InvoiceNo").alias("NbInvoices")
)
# Création de la variable cible (binaire)
# Seuil : 75e percentile du revenu total
threshold = customers.approxQuantile("TotalRevenue", [0.75], 0.01)[0]
customers = customers.withColumn("Label",
when(col("TotalRevenue") > threshold, 1).otherwise(0))
# Assemblage des features en vecteur
assembler = VectorAssembler(
inputCols=["TotalQuantity", "AvgUnitPrice", "NbInvoices"],
outputCol="features"
)
# Modèle de classification
lr = LogisticRegression(featuresCol="features", labelCol="Label", maxIter=20)
# Pipeline d'entraînement
pipeline = Pipeline(stages=[assembler, lr])
train, test = customers.randomSplit([0.7, 0.3], seed=42)
model = pipeline.fit(train)
# Évaluation
predictions = model.transform(test)
auc = BinaryClassificationEvaluator(metricName="areaUnderROC").evaluate(predictions)
print(f"AUC: {auc}") # Résultat obtenu : ~0.92