# Makefile for MinIO deployment

NAMESPACE ?= data-platform
AIRFLOW_OPERATOR ?= apache-airflow/airflow

# Optional targets for specific components
.PHONY: build-custom-dockerfile install uninstall

build-custom-dockerfile:
	@set -e; set -x; \
	docker build --progress=plain \
		-t airflow-custom:2.10.5 \
		-f infra/services/airflow/operator/Dockerfile .

install:
	@set -e; set -x; \
	kubectl delete secret my-webserver-secret --namespace $(NAMESPACE) || true; \
	kubectl create secret generic my-webserver-secret \
		--from-literal="webserver-secret-key=$(python3 -c 'import secrets; print(secrets.token_hex(16))')" \
		--namespace $(NAMESPACE); \
	helm upgrade --install --namespace $(NAMESPACE) \
		airflow-operator $(AIRFLOW_OPERATOR) \
		--set dags.persistence.enabled=false \
		--set dags.gitSync.enabled=true \
		--set dags.gitSync.repo=https://github.com/lam1051999/data-platform \
		--set dags.gitSync.branch=main \
		--set dags.gitSync.subPath=pipeline/airflow \
		--set pgbouncer.enabled=true \
		--set webserverSecretKeySecretName=my-webserver-secret \
		--set workers.safeToEvict=true \
		--set scheduler.safeToEvict=true \
		--set triggerer.safeToEvict=true \
		--set dagProcessor.safeToEvict=true \
		--set redis.safeToEvict=true \
		--set images.airflow.repository=airflow-custom \
		--set images.airflow.tag=2.10.5 \
		--set webserver.defaultUser.username=admin \
		--set webserver.defaultUser.password=admin

uninstall:
	@set -e; set -x; \
	helm uninstall --namespace $(NAMESPACE) \
		airflow-operator