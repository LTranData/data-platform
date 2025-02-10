# Makefile for Spark deployment

NAMESPACE ?= data-platform

# Optional targets for specific components
.PHONY: install uninstall

install:
	@set -e; set -x; \
	helm upgrade --install --namespace $(NAMESPACE) \
		--values infra/services/spark/values.yaml \
    	spark-operator spark-operator/spark-operator

uninstall:
	@set -e; set -x; \
	helm uninstall --namespace $(NAMESPACE) \
		spark-operator