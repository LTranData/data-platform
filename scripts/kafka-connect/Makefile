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
		-f infra/services/kafka-connect/values.yaml

uninstall:
	@set -ex; \
	helm uninstall --namespace $(NAMESPACE) \
		kafka-connect-operator