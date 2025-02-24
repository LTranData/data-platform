# Makefile for Kafka Connect

NAMESPACE ?= data-platform

# Optional targets for specific components
.PHONY: install uninstall build-custom-dockerfile

build-custom-dockerfile:
	@set -ex; \
	docker build --progress=plain \
		-t lam1051999/kafka-connect-custom:7.9.0 \
		-f infra/services/kafka-connect/Dockerfile .

install:
	@set -ex; \
	helm upgrade --install --namespace $(NAMESPACE) \
		kafka-connect-operator infra/services/kafka-connect/ \
		--set configurationOverrides.key.converter=org.apache.kafka.connect.json.JsonConverter \
		--set configurationOverrides.value.converter=org.apache.kafka.connect.json.JsonConverter \
		--set configurationOverrides.producer.security.protocol=SASL_SSL \
		--set configurationOverrides.producer.sasl.mechanism=SCRAM-SHA-512 \
		--set configurationOverrides.producer.sasl.jaas.config="org.apache.kafka.common.security.scram.ScramLoginModule required username=\"brokerUser\" password=\"brokerPassword\";" \
		--set configurationOverrides.producer.ssl.truststore.type=JKS \
		--set configurationOverrides.producer.ssl.truststore.location=/usr/share/confluent-hub-components/kafka.truststore.jks \
		--set configurationOverrides.producer.ssl.truststore.password=changeit \
		--set configurationOverrides.producer.ssl.keystore.type=JKS \
		--set configurationOverrides.producer.ssl.keystore.location=/usr/share/confluent-hub-components/kafka.keystore.jks \
		--set configurationOverrides.producer.ssl.keystore.password=changeit \
		--set configurationOverrides.consumer.security.protocol=SASL_SSL \
		--set configurationOverrides.consumer.sasl.mechanism=SCRAM-SHA-512 \
		--set configurationOverrides.consumer.sasl.jaas.config="org.apache.kafka.common.security.scram.ScramLoginModule required username=\"brokerUser\" password=\"brokerPassword\";" \
		--set configurationOverrides.consumer.ssl.truststore.type=JKS \
		--set configurationOverrides.consumer.ssl.truststore.location=/usr/share/confluent-hub-components/kafka.truststore.jks \
		--set configurationOverrides.consumer.ssl.truststore.password=changeit \
		--set configurationOverrides.consumer.ssl.keystore.type=JKS \
		--set configurationOverrides.consumer.ssl.keystore.location=/usr/share/confluent-hub-components/kafka.keystore.jks \
		--set configurationOverrides.consumer.ssl.keystore.password=changeit \
		--set kafka.bootstrapServers=SASL_SSL://kafka-operator.data-platform.svc.cluster.local:9092 \
		--set image=lam1051999/kafka-connect-custom \
		--set imageTag==7.9.0