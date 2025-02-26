FROM confluentinc/cp-kafka-connect:7.9.0

RUN confluent-hub install --no-prompt debezium/debezium-connector-mongodb:latest
RUN confluent-hub install --no-prompt debezium/debezium-connector-mysql:latest
RUN confluent-hub install --no-prompt debezium/debezium-connector-postgresql:latest
RUN confluent-hub install --no-prompt debezium/debezium-connector-sqlserver:latest

COPY scripts/kafka/kafka.truststore.jks /usr/share/confluent-hub-components/kafka.truststore.jks
COPY scripts/kafka/kafka.keystore.jks /usr/share/confluent-hub-components/kafka.keystore.jks