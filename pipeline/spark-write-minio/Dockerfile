FROM LTranData/spark-application:3.5.3

USER root
WORKDIR /app

RUN apt-get update && \
    apt install -y python3 python3-pip && \
    pip3 install --upgrade pip setuptools && \
    # Removed the .cache to save space
    rm -rf /root/.cache && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/*

# Install Python libraries
COPY pipeline/spark-write-minio/requirements.txt .
RUN pip3 install -r /app/requirements.txt

# Add Delta Lake
ADD https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.3.0/delta-spark_2.12-3.3.0.jar $SPARK_HOME/jars
ADD https://repo1.maven.org/maven2/io/delta/delta-storage/3.3.0/delta-storage-3.3.0.jar $SPARK_HOME/jars
# Add AWS jars
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar $SPARK_HOME/jars
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.172/aws-java-sdk-bundle-1.12.172.jar $SPARK_HOME/jars
ADD https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/2.17.257/bundle-2.17.257.jar $SPARK_HOME/jars
ADD https://repo1.maven.org/maven2/software/amazon/awssdk/url-connection-client/2.17.257/url-connection-client-2.17.257.jar $SPARK_HOME/jars
# Support for S3 magic committer...
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-hadoop-cloud_2.12/3.3.4/spark-hadoop-cloud_2.12-3.3.4.jar $SPARK_HOME/jars

RUN chmod -R 644 $SPARK_HOME/jars/*

# Copy main application
COPY pipeline/spark-write-minio/generate_data.py .

# Certificate import
COPY scripts/minio/selfsigned.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
RUN keytool -importcert -alias minio-ca -file /usr/local/share/ca-certificates/selfsigned.crt \
    -keystore $JAVA_HOME/lib/security/cacerts \
    -storepass changeit -noprompt