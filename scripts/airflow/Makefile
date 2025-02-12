# Makefile for MinIO deployment

NAMESPACE ?= data-platform
AIRFLOW_OPERATOR ?= apache-airflow/airflow

# Optional targets for specific components
.PHONY: build-custom-dockerfile install uninstall release-docker-images create-clusterrolebinding-for-spark-applications

build-custom-dockerfile:
	@set -ex; \
	docker build --progress=plain \
		-t lam1051999/airflow-custom:2.10.5 \
		-f infra/services/airflow/operator/Dockerfile .

install:
	@set -ex; \
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
		--set images.airflow.repository=lam1051999/airflow-custom \
		--set images.airflow.tag=2.10.5 \
		--set webserver.defaultUser.username=admin \
		--set webserver.defaultUser.password=admin

uninstall:
	@set -ex; \
	helm uninstall --namespace $(NAMESPACE) \
		airflow-operator

release-docker-images:
	@set -ex; \
	docker push lam1051999/airflow-custom:2.10.5

create-clusterrolebinding-for-spark-applications:
	@set -ex; \
	kubectl create clusterrolebinding default-admin \
		--clusterrole cluster-admin \
		--serviceaccount=$(NAMESPACE):airflow-operator-worker \
		--namespace $(NAMESPACE)