# Makefile for Airflow deployment

NAMESPACE ?= data-platform
AIRFLOW_OPERATOR ?= apache-airflow/airflow
WEBSERVER_SECRET_KEY ?=63c426f3362ccd39191fb77476845bae
FERNET_KEY ?=DUqWeirPBeArHja24wrtiMH0idTjOf-Gs6xUPnhxxNc=

# Optional targets for specific components
.PHONY: build-custom-dockerfile install uninstall release-docker-images create-clusterrolebinding-for-spark-applications

build-custom-dockerfile:
	@set -ex; \
	docker build --progress=plain \
		-t LTranData/airflow-custom:2.10.5 \
		-f infra/services/airflow/operator/Dockerfile .

install:
	@set -ex; \
	kubectl delete secret my-webserver-secret --namespace $(NAMESPACE) || true; \
	kubectl create secret generic my-webserver-secret \
		--from-literal="webserver-secret-key=$(WEBSERVER_SECRET_KEY)" \
		--namespace $(NAMESPACE); \
	kubectl delete secret airflow-fernet-key --namespace $(NAMESPACE) || true; \
	kubectl create secret generic airflow-fernet-key \
		--from-literal="fernet-key=$(FERNET_KEY)" \
		--namespace $(NAMESPACE); \
	helm upgrade --install --namespace $(NAMESPACE) \
		airflow-operator $(AIRFLOW_OPERATOR) \
		--set dags.persistence.enabled=false \
		--set dags.gitSync.enabled=true \
		--set dags.gitSync.repo=https://github.com/LTranData/data-platform \
		--set dags.gitSync.branch=main \
		--set dags.gitSync.subPath=pipeline/airflow \
		--set pgbouncer.enabled=true \
		--set webserverSecretKeySecretName=my-webserver-secret \
		--set workers.safeToEvict=true \
		--set scheduler.safeToEvict=true \
		--set triggerer.safeToEvict=true \
		--set dagProcessor.safeToEvict=true \
		--set redis.safeToEvict=true \
		--set images.airflow.repository=LTranData/airflow-custom \
		--set images.airflow.tag=2.10.5 \
		--set webserver.defaultUser.username=admin \
		--set webserver.defaultUser.password=admin \
		--set fernetKeySecretName=airflow-fernet-key

uninstall:
	@set -ex; \
	helm uninstall --namespace $(NAMESPACE) \
		airflow-operator

release-docker-images:
	@set -ex; \
	docker push LTranData/airflow-custom:2.10.5

create-clusterrolebinding-for-spark-applications:
	@set -ex; \
	kubectl create clusterrolebinding default-admin \
		--clusterrole cluster-admin \
		--serviceaccount=$(NAMESPACE):airflow-operator-worker \
		--namespace $(NAMESPACE)