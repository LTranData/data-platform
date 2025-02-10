from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType
from faker import Faker
import random
import os

# Initialize Spark Session with Delta Lake support
spark: SparkSession = SparkSession.builder.enableHiveSupport().getOrCreate()

# MinIO configuration
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID", "minio"))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY", "minio123"))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", os.getenv("ENDPOINT", "https://localhost:9000"))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "true")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.attempts.maximum", "1")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.establish.timeout", "5000")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.timeout", "10000")

# Initialize Faker
fake = Faker()

# Define schema for the data
schema = StructType([
    StructField("user_id", StringType(), False),
    StructField("name", StringType(), False),
    StructField("email", StringType(), False),
    StructField("address", StringType(), False),
    StructField("phone_number", StringType(), False),
    StructField("age", IntegerType(), False),
    StructField("registration_date", DateType(), False)
])

# Function to generate fake data
def generate_fake_data(num_records):
    data = []
    for _ in range(num_records):
        data.append((
            fake.uuid4(),
            fake.name(),
            fake.email(),
            fake.address().replace('\n', ', '),
            fake.phone_number(),
            random.randint(18, 80),
            fake.date_between(start_date='-5y', end_date='today')
        ))
    return data

# Generate sample data
num_records = 5
fake_data = generate_fake_data(num_records)

# Create DataFrame from the generated data
df = spark.createDataFrame(fake_data, schema=schema)

# Write the data to Delta format
df.repartition(1) \
    .write \
    .format("delta") \
    .mode("append") \
    .save("s3a://mybucket/user_data")

print("Sample data from Delta table:")
df.show(10, truncate=False)
print("Number of records: ", df.count())