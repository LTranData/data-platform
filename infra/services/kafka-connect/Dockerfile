FROM confluentinc/cp-kafka-connect:7.9.0

USER root:root

RUN mkdir -p /usr/share/confluent-hub-components/debezium/

ADD https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/3.0.7.Final/debezium-connector-postgres-3.0.7.Final-plugin.tar.gz /tmp/
RUN tar -xvf /tmp/debezium-connector-postgres-3.0.7.Final-plugin.tar.gz -C /tmp/ && \
    cp -r /tmp/debezium-connector-postgres/* /usr/share/confluent-hub-components/debezium/

COPY scripts/kafka/kafka.keystore.jks /usr/share/confluent-hub-components/
COPY scripts/kafka/kafka.truststore.jks /usr/share/confluent-hub-components/
    
USER 1001