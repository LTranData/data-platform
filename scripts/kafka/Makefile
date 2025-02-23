# Makefile for Kafka deployment

NAMESPACE ?= data-platform
KAFKA_OPERATOR ?= bitnami/kafka
STORE_PASSWORD ?= changeit

# Optional targets for specific components
.PHONY: install uninstall generate-self-signed-cert-keystore-truststore register-self-signed-cert-keystore-truststore create-kafka-client-pod

install:
	@set -ex; \
	helm upgrade --install --namespace $(NAMESPACE) \
		kafka-operator $(KAFKA_OPERATOR) \
		--set listeners.client.protocol=SASL_SSL \
		--set listeners.controller.protocol=SSL \
		--set listeners.interbroker.protocol=SSL \
		--set listeners.external.protocol=SASL_SSL \
		--set sasl.client.users[0]=brokerUser \
		--set sasl.client.passwords[0]=brokerPassword \
		--set tls.existingSecret=kafka-jks \
		--set tls.keystorePassword=$(STORE_PASSWORD) \
		--set tls.truststorePassword=$(STORE_PASSWORD) \
		--set externalAccess.enabled=true \
		--set externalAccess.controller.service.type=NodePort \
		--set externalAccess.broker.service.type=NodePort \
		--set externalAccess.autoDiscovery.enabled=true \
		--set controller.automountServiceAccountToken=true \
		--set broker.automountServiceAccountToken=true \
		--set serviceAccount.create=true \
		--set rbac.create=true

uninstall:
	@set -ex; \
	helm uninstall --namespace $(NAMESPACE) \
		kafka-operator

generate-self-signed-cert-keystore-truststore:
	@set -ex; \
	rm scripts/kafka/*.jks; \
	openssl req -new -x509 -nodes -days 730 -keyout scripts/kafka/kafka.key \
		-out scripts/kafka/kafka.crt \
		-config scripts/kafka/openssl.conf; \
	openssl pkcs12 -export -in scripts/kafka/kafka.crt \
		-inkey scripts/kafka/kafka.key \
		-out scripts/kafka/kafka.p12 \
		-passout pass:$(STORE_PASSWORD) -name kafka; \
	keytool -importkeystore -srckeystore scripts/kafka/kafka.p12 \
		-destkeystore scripts/kafka/kafka.keystore.jks \
		-srcstoretype pkcs12 \
		-deststorepass $(STORE_PASSWORD) \
		-srcstorepass $(STORE_PASSWORD) \
		-alias kafka -noprompt; \
	rm scripts/kafka/kafka.p12; \
	keytool -importcert -alias kafka -file scripts/kafka/kafka.crt \
		-keystore scripts/kafka/kafka.truststore.jks \
		-storepass $(STORE_PASSWORD) -noprompt


register-self-signed-cert-keystore-truststore:
	@set -ex; \
	kubectl delete secret kafka-jks --namespace $(NAMESPACE) || true; \
	kubectl create secret generic kafka-jks \
		--from-file=kafka.truststore.jks=scripts/kafka/kafka.truststore.jks \
		--from-file=kafka.keystore.jks=scripts/kafka/kafka.keystore.jks \
		--namespace $(NAMESPACE)

create-kafka-client-pod:
	@set -ex; \
	kubectl delete pod kafka-operator-client -n $(NAMESPACE) || true; \
	kubectl run kafka-operator-client \
		--restart='Never' \
		--image docker.io/bitnami/kafka:3.9.0-debian-12-r6 \
		-n $(NAMESPACE) --command -- sleep infinity; \
	sleep 5; \
	kubectl cp -n $(NAMESPACE) \
		scripts/kafka/client.properties kafka-operator-client:/tmp/client.properties; \
	kubectl cp -n $(NAMESPACE) \
		scripts/kafka/kafka.truststore.jks kafka-operator-client:/tmp/kafka.truststore.jks; \
	kubectl cp -n $(NAMESPACE) \
		scripts/kafka/kafka.keystore.jks kafka-operator-client:/tmp/kafka.keystore.jks; \
	kubectl exec --tty -i \
		kafka-operator-client \
		-n $(NAMESPACE) -- bash