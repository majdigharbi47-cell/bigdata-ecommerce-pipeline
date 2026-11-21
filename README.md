# End-to-End Big Data Pipeline: Batch, Streaming & ML on E-Commerce Data

[![Hadoop](https://img.shields.io/badge/Apache%20Hadoop-3.2.1-yellow?logo=apachehadoop)](https://hadoop.apache.org/)
[![Spark](https://img.shields.io/badge/Apache%20Spark-3.3.0-orange?logo=apachespark)](https://spark.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python)](https://www.python.org/)

Distributed Big Data pipeline built with **Docker**, **Apache Hadoop (HDFS, MapReduce)**, and **Apache Spark (PySpark, MLlib, Structured Streaming)** using the **Online Retail** dataset (541,909 e-commerce transactions).

---

## Architecture Overview

1. **Cluster Deployment (`Docker Compose`)**: Multi-node virtualized infrastructure with **1 NameNode**, **2 DataNodes** (HDFS replication factor = 2), **1 Spark Master**, and **1 Spark Worker** communicating over an isolated bridge network (`hadoop-network`).
2. **Batch Descriptive Analytics (`Hadoop MapReduce` + Python Streaming)**:
   - **Revenue by Country**: Filters cancelled invoices (`InvoiceNo` starting with `C`) and invalid quantities/prices, aggregating total revenue per country.
   - **Top 10 Best-Selling Products**: Uses a bounded min-heap (`heapq`, $O(n \log 10)$) in the Reducer to extract the top 10 products by sold volume without sorting the entire dataset in memory.
3. **Predictive Analytics (`PySpark MLlib`)**: Aggregates customer purchase behavior (`TotalRevenue`, `TotalQuantity`, `AvgUnitPrice`, `NbInvoices`), labels high-value customers above the 75th percentile revenue threshold, and trains a classification model via Spark `Pipeline`.
4. **Real-Time Analytics (`Spark Structured Streaming`)**: Watches `/stream_input` in HDFS and performs stateful aggregations as new CSV micro-batches arrive.
5. **Visualization (`Matplotlib` & `Seaborn`)**: Exports HDFS outputs to local storage and generates high-resolution figures (top countries, top products, and confusion matrix).

---

## Project Structure

```text
bigdata-ecommerce-pipeline/
├── docker-compose.yml
├── hadoop.env
├── README.md
├── docs/
│   └── projet big data
├── mapreduce/
│   ├── mapper_revenue_country.py
│   ├── reducer_revenue.py
│   ├── mapper_top_products.py
│   └── reducer_top_products.py
├── spark/
│   ├── predictive_model.py
│   └── streaming_revenue.py
├── visualization/
│   └── plot_results.py
└── results/
    └── figures/
        ├── FIGURE 1  Top Pays par Revenue
        ├── FIGURE 2  Top Produits
        └── FIGURE 3  Matrice de Confusion (ML)