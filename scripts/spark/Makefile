# Makefile for Spark deployment

NAMESPACE ?= data-platform

# Optional targets for specific components
.PHONY: install uninstall build-spark-application-dockerfile build-spark-write-minio-dockerfile

install:
	@set -e; set -x; \
	helm upgrade --install --namespace $(NAMESPACE) \
		--values infra/services/spark/operator/values.yaml \
    	spark-operator spark-operator/spark-operator

uninstall:
	@set -e; set -x; \
	helm uninstall --namespace $(NAMESPACE) \
		spark-operator

build-spark-application-dockerfile:
	@set -e; set -x; \
	export EXISTING_PWD=$(pwd); \
	cd $(SPARK_HOME); \
	docker build --progress=plain \
		-t spark-application:3.5.3 \
		-f kubernetes/dockerfiles/spark/Dockerfile .; \
	cd $(EXISTING_PWD)

build-spark-write-minio-dockerfile:
	@set -e; set -x; \
	docker build --progress=plain \
		-t spark-write-minio:3.5.3 \
		-f pipeline/spark-write-minio/Dockerfile .;