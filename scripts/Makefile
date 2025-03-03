# Makefile for project

NAMESPACE ?= data-platform

# Optional targets for specific components
.PHONY: install uninstall

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
	make -f scripts/minio/Makefile uninstall; \
	make -f scripts/spark/Makefile uninstall; \
	make -f scripts/airflow/Makefile uninstall; \
	make -f scripts/hive/Makefile uninstall; \
	make -f scripts/kafka/Makefile uninstall; \
	make -f scripts/sources/Makefile uninstall-postgres; \
	make -f scripts/kafka-connect/Makefile uninstall; \
	make -f scripts/trino/Makefile uninstall