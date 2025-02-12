FROM openjdk:8-slim

ARG HADOOP_VERSION=3.2.0

RUN apt-get update && \
    apt-get install -y curl --no-install-recommends && \
    apt-get install -y gettext-base --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Download and extract the Hadoop binary package
RUN curl https://archive.apache.org/dist/hadoop/core/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz | tar xvz -C /opt/ && \
    ln -s /opt/hadoop-$HADOOP_VERSION /opt/hadoop && \
    rm -r /opt/hadoop/share/doc

# Add S3a jars to the classpath using this hack
RUN ln -s /opt/hadoop/share/hadoop/tools/lib/hadoop-aws* /opt/hadoop/share/hadoop/common/lib/ && \
    ln -s /opt/hadoop/share/hadoop/tools/lib/aws-java-sdk* /opt/hadoop/share/hadoop/common/lib/

# Set necessary environment variables
ENV HADOOP_HOME="/opt/hadoop"
ENV PATH="/opt/spark/bin:/opt/hadoop/bin:${PATH}"

# Download and install the standalone metastore binary
RUN curl https://archive.apache.org/dist/hive/hive-standalone-metastore-3.0.0/hive-standalone-metastore-3.0.0-bin.tar.gz | tar xvz -C /opt/ && \
    ln -s /opt/apache-hive-metastore-3.0.0-bin /opt/hive-metastore

# Download PostgreSQL JDBC driver
ADD https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar /opt/hadoop/share/hadoop/common/lib/
ADD https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar /opt/hive-metastore/lib

# For org.apache.hadoop.hive.ql.optimizer.ppr.PartitionExpressionForMetastore
ADD https://repo1.maven.org/maven2/org/apache/hive/hive-exec/3.0.0/hive-exec-3.0.0.jar /opt/hive-metastore/lib

# Add customized configuration
COPY infra/services/hive/metastore/conf/entrypoint.sh /opt/
COPY infra/services/hive/metastore/conf/bootstrap.sh /opt/
COPY infra/services/hive/metastore/conf/core-site.xml /opt/hadoop/etc/hadoop/
COPY infra/services/hive/metastore/conf/metastore-site.xml /opt/hive-metastore/conf/

# Certificate import
COPY scripts/minio/selfsigned.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
RUN keytool -importcert -alias minio-ca -file /usr/local/share/ca-certificates/selfsigned.crt \
    -keystore $JAVA_HOME/lib/security/cacerts \
    -storepass changeit -noprompt