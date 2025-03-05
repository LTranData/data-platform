# Makefile for project

NAMESPACE ?= data-platform

# Optional targets for specific components
.PHONY: init install uninstall expose-ports

init:
	@set -ex; \
	make -f scripts/minio/Makefile generate-self-signed-cert; \
	make -f scripts/minio/Makefile register-self-signed-cert; \
	make -f scripts/spark/Makefile build-spark-application-dockerfile; \
	make -f scripts/spark/Makefile build-spark-write-minio-dockerfile; \
	make -f scripts/spark/Makefile release-docker-images; \
	make -f scripts/airflow/Makefile build-custom-dockerfile; \
	make -f scripts/airflow/Makefile release-docker-images; \
	make -f scripts/hive/Makefile build-metastore-custom-dockerfile; \
	make -f scripts/hive/Makefile build-schematool-custom-dockerfile; \
	make -f scripts/hive/Makefile release-docker-images; \
	make -f scripts/spark/Makefile build-spark-create-hive-table-dockerfile; \
	make -f scripts/kafka/Makefile generate-self-signed-cert-keystore-truststore; \
	make -f scripts/kafka/Makefile register-self-signed-cert-keystore-truststore; \
	make -f scripts/trino/Makefile build-trino-custom-dockerfile; \
	make -f scripts/trino/Makefile release-docker-images

install:
	@set -ex; \
	make -f scripts/minio/Makefile install; \
	make -f scripts/spark/Makefile install; \
	make -f scripts/airflow/Makefile install; \
	make -f scripts/hive/Makefile install; \
	make -f scripts/kafka/Makefile install; \
	make -f scripts/sources/Makefile install-postgres; \
	make -f scripts/kafka-connect/Makefile install; \
	make -f scripts/trino/Makefile install

uninstall:
	@set -ex; \
	make -f scripts/minio/Makefile uninstall || true; \
	make -f scripts/spark/Makefile uninstall || true; \
	make -f scripts/airflow/Makefile uninstall || true; \
	make -f scripts/hive/Makefile uninstall || true; \
	make -f scripts/kafka/Makefile uninstall || true; \
	make -f scripts/sources/Makefile uninstall-postgres || true; \
	make -f scripts/kafka-connect/Makefile uninstall || true; \
	make -f scripts/trino/Makefile uninstall || true

expose-ports:
	@set -ex; \
	lsof -t -i tcp:9000 | xargs kill; \
	lsof -t -i tcp:9443 | xargs kill; \
	lsof -t -i tcp:8080 | xargs kill; \
	lsof -t -i tcp:5432 | xargs kill; \
	lsof -t -i tcp:8083 | xargs kill; \
	lsof -t -i tcp:8089 | xargs kill; \
	kubectl port-forward service/myminio-hl 9000 -n data-platform &
	kubectl port-forward service/myminio-console 9443 -n data-platform &
	kubectl port-forward service/airflow-operator-webserver 8080 -n data-platform &
	kubectl port-forward service/postgres-source-postgresql 5432 -n data-platform &
	kubectl port-forward service/kafka-connect-operator-cp-kafka-connect 8083 -n data-platform &
	kubectl port-forward service/trino-operator-trino 8089:8080 -n data-platform &