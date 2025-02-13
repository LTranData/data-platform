from pyspark.sql import SparkSession
import os

# Initialize Spark Session with Hive support
spark = SparkSession.builder \
    .appName("HiveCreateTableExample") \
    .config("hive.metastore.uris", "thrift://hive-metastore.data-platform.svc.cluster.local:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# MinIO configuration
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID", "minio"))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY", "minio123"))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", os.getenv("ENDPOINT", "https://localhost:9000"))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "true")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.attempts.maximum", "1")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.establish.timeout", "5000")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.timeout", "10000")

# Create a simple DataFrame (replace with your data)
data = [("Alice", 25), ("Bob", 30), ("Charlie", 28)]
df = spark.createDataFrame(data, ["name", "age"])

# Create a Hive table
table_name = "my_hive_table"  # Choose your table name
database_name = "default" # Choose your database name. Default is used if you don't specify one.

# Method 1: Using SQL syntax (Recommended for flexibility)
spark.sql(f"CREATE TABLE IF NOT EXISTS {database_name}.{table_name} (name STRING, age INT) STORED AS ORC") # ORC is a good default format
# ORC is a good default format. You can also use other formats like PARQUET, AVRO, etc.
# IF NOT EXISTS clause ensures that the table is not recreated if it already exists.

# Insert data into the table
df.write.mode("overwrite").insertInto(database_name, table_name) # Overwrite if the table already has data. Append if you want to add new data.

# Method 2: Using DataFrame API (Less flexible, but sometimes simpler for basic cases)
# df.write.mode("overwrite").saveAsTable(table_name) # This creates the table if it doesn't exist.

# Show all tables in the default database
spark.sql("SHOW TABLES").show()

# Show all tables in a specific database:
spark.sql(f"SHOW TABLES IN {database_name}").show()

# Show tables with a specific pattern (e.g., all tables starting with "my_"):
spark.sql("SHOW TABLES LIKE 'my_*'").show()

# Describe the table schema
spark.sql(f"DESCRIBE {database_name}.{table_name}").show()

# Query the data from the Hive table
spark.sql(f"SELECT * FROM {database_name}.{table_name}").show()

# Stop the Spark session
spark.stop()