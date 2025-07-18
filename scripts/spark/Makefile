# Makefile for Spark deployment

NAMESPACE ?= data-platform
SPARK_OPERATOR ?= spark-operator/spark-operator

# Optional targets for specific components
.PHONY: install uninstall build-spark-application-dockerfile build-spark-write-minio-dockerfile build-spark-create-hive-table-dockerfile release-docker-images

install:
	@set -ex; \
	helm upgrade --install --namespace $(NAMESPACE) \
		--values infra/services/spark/operator/values.yaml \
    	spark-operator $(SPARK_OPERATOR)

uninstall:
	@set -ex; \
	helm uninstall --namespace $(NAMESPACE) \
		spark-operator

build-spark-application-dockerfile:
	@set -ex; \
	export EXISTING_PWD=$(pwd); \
	cd $(SPARK_HOME); \
	docker build --progress=plain \
		-t LTranData/spark-application:3.5.3 \
		-f kubernetes/dockerfiles/spark/Dockerfile .; \
	cd $(EXISTING_PWD)

build-spark-write-minio-dockerfile:
	@set -ex; \
	docker build --progress=plain \
		-t LTranData/spark-write-minio:3.5.3 \
		-f pipeline/spark-write-minio/Dockerfile .; \
	kubectl delete secret minio-secret --namespace $(NAMESPACE) || true; \
	kubectl create secret generic minio-secret \
		--from-literal=AWS_ACCESS_KEY_ID=minio \
		--from-literal=AWS_SECRET_ACCESS_KEY=minio123 \
		--from-literal=ENDPOINT=https://minio.data-platform.svc.cluster.local:443 \
		--from-literal=AWS_REGION=us-east-1 \
		--namespace $(NAMESPACE)

build-spark-create-hive-table-dockerfile:
	@set -ex; \
	docker build --progress=plain \
		-t LTranData/spark-create-hive-table:3.5.3 \
		-f pipeline/spark-create-hive-table/Dockerfile .

release-docker-images:
	@set -ex; \
	docker push LTranData/spark-application:3.5.3; \
	docker push LTranData/spark-write-minio:3.5.3; \
	docker push LTranData/spark-create-hive-table:3.5.3