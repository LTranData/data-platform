# Makefile for Trino deployment

NAMESPACE ?= data-platform
TRINO_OPERATOR ?= trino/trino

# Optional targets for specific components
.PHONY: build-trino-custom-dockerfile install uninstall

build-trino-custom-dockerfile:
	@set -ex; \
	docker build --progress=plain \
		-t LTranData/trino-custom:470 \
		-f infra/services/trino/operator/Dockerfile .

install:
	@set -ex; \
	helm upgrade --install --namespace $(NAMESPACE) \
		trino-operator $(TRINO_OPERATOR) \
		  -f infra/services/trino/operator/catalogs.yaml

uninstall:
	@set -ex; \
	helm uninstall --namespace $(NAMESPACE) \
		trino-operator

release-docker-images:
	@set -ex; \
	docker push LTranData/trino-custom:470