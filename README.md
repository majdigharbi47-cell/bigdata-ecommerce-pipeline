# End-to-End Big Data Pipeline: Batch, Streaming & ML on E-Commerce Data

Distributed Big Data pipeline built with **Docker**, **Apache Hadoop (HDFS, MapReduce)**, and **Apache Spark (PySpark, MLlib, Structured Streaming)** using the **Online Retail** dataset (541,909 transactions).

## Architecture Overview

1. **Storage & Cluster Setup (`Docker Compose`)**: 1 NameNode, 2 DataNodes (replication factor = 2), 1 Spark Master, and 1 Spark Worker connected over an isolated `hadoop-network`.
2. **Batch Descriptive Analytics (`Hadoop MapReduce` + Python)**:
   - **Revenue by Country**: Filters cancelled invoices (`InvoiceNo` starting with `C`) and invalid quantities/prices, then aggregates revenue per country.
   - **Top 10 Best-Selling Products**: Uses a bounded min-heap (`heapq`, $O(n \log 10)$) to extract the top 10 products by total quantity sold.
3. **Predictive Analytics (`PySpark MLlib`)**: Aggregates customer purchase behavior (`TotalRevenue`, `TotalQuantity`, `AvgUnitPrice`, `NbInvoices`), labels high-value customers above the 75th percentile revenue threshold, and trains a classification model (`Pipeline` + `LogisticRegression`).
4. **Real-Time Analytics (`Spark Structured Streaming`)**: Watches `/stream_input` in HDFS and performs stateful aggregations as new CSV micro-batches arrive.
5. **Visualization (`Matplotlib` & `Seaborn`)**: Exports results from HDFS and generates charts for top countries, top products, and the confusion matrix.

## Project Structure

```text
bigdata-ecommerce-pipeline/
├── docker-compose.yml
├── hadoop.env
├── README.md
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