# Makefile for Hive metastore deployment

NAMESPACE ?= data-platform
POSTGRES_OPERATOR ?= bitnami/postgresql

# Optional targets for specific components
.PHONY: build-metastore-custom-dockerfile build-schematool-custom-dockerfile install uninstall release-docker-images

build-metastore-custom-dockerfile:
	@set -ex; \
	kubectl delete secret hive-metastore-secret --namespace $(NAMESPACE) || true; \
	kubectl create secret generic hive-metastore-secret \
		--from-literal=POSTGRES_URL=jdbc:postgresql://hive-metastore-postgres-postgresql.data-platform.svc.cluster.local:5432/metastore \
		--from-literal=POSTGRES_USERNAME=postgres \
		--from-literal=POSTGRES_PASSWORD=postgres \
		--from-literal=S3_WAREHOUSE_DIR=s3a://hive-warehouse \
		--namespace $(NAMESPACE); \
	docker build --progress=plain \
		-t lam1051999/hive-metastore-custom:3.0.0 \
		-f infra/services/hive/metastore/Dockerfile .

build-schematool-custom-dockerfile:
	@set -ex; \
	docker build --progress=plain \
		-t lam1051999/hive-schematool-custom:4.0.0 \
		-f infra/services/hive/schematool/Dockerfile .

install:
	@set -ex; \
	helm upgrade --install --namespace $(NAMESPACE) \
		hive-metastore-postgres $(POSTGRES_OPERATOR) \
		--set global.postgresql.auth.postgresPassword=postgres \
		--set global.postgresql.auth.database=metastore; \
	kubectl apply -f infra/services/hive/schematool/job.yaml; \
	kubectl apply -f infra/services/hive/metastore/deployment.yaml; \
	kubectl apply -f infra/services/hive/metastore/service.yaml

uninstall:
	@set -ex; \
	kubectl delete -f infra/services/hive/metastore/service.yaml; \
	kubectl delete -f infra/services/hive/metastore/deployment.yaml; \
	kubectl delete -f infra/services/hive/schematool/job.yaml; \
	helm uninstall --namespace $(NAMESPACE) \
		hive-metastore-postgres

release-docker-images:
	@set -ex; \
	docker push lam1051999/hive-metastore-custom:3.0.0; \
	docker push lam1051999/hive-schematool-custom:4.0.0