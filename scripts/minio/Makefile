# Makefile for MinIO deployment

NAMESPACE ?= data-platform
MINIO_OPERATOR ?= minio-operator/operator
MINIO_TENANT ?= minio-operator/tenant

# Optional targets for specific components
.PHONY: install uninstall install-operator install-tenant uninstall-operator uninstall-tenant generate-self-signed-certs register-self-signed-cert

install: install-operator install-tenant
uninstall: uninstall-operator uninstall-tenant

install-operator:
	@set -e; set -x; \
	helm upgrade --install --namespace $(NAMESPACE) \
		--values infra/services/minio/operator/values.yaml \
		minio-operator $(MINIO_OPERATOR)

install-tenant:
	@set -e; set -x; \
	helm upgrade --install --namespace $(NAMESPACE) \
		--values infra/services/minio/tenant/values.yaml \
		minio-tenant $(MINIO_TENANT)

uninstall-operator:
	@set -e; set -x; \
	helm uninstall --namespace $(NAMESPACE) \
		minio-operator

uninstall-tenant:
	@set -e; set -x; \
	helm uninstall --namespace $(NAMESPACE) \
		minio-tenant

generate-self-signed-cert:
	@set -e; set -x; \
	openssl req -new -nodes \
		-newkey rsa:2048 \
		-keyout scripts/minio/selfsigned.key \
		-out scripts/minio/selfsigned.csr \
		-config scripts/minio/openssl.conf; \
	openssl x509 -req \
		-in scripts/minio/selfsigned.csr \
		-signkey scripts/minio/selfsigned.key \
		-out scripts/minio/selfsigned.crt \
		-days 365 \
		-sha256 \
		-extfile scripts/minio/openssl.conf \
		-extensions req_ext

register-self-signed-cert:
	@set -e; set -x; \
	kubectl delete secret minio-selfsigned-secret --namespace $(NAMESPACE); \
	kubectl create secret tls minio-selfsigned-secret \
		--key scripts/minio/selfsigned.key \
		--cert scripts/minio/selfsigned.crt \
		--namespace $(NAMESPACE)