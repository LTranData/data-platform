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
	openssl req -new -x509 -nodes -days 730 -keyout scripts/minio/selfsigned.key \
		-out scripts/minio/selfsigned.crt \
		-config scripts/minio/openssl.conf

register-self-signed-cert:
	@set -e; set -x; \
	kubectl delete secret minio-selfsigned-secret --namespace $(NAMESPACE) || true; \
	kubectl create secret tls minio-selfsigned-secret \
		--key scripts/minio/selfsigned.key \
		--cert scripts/minio/selfsigned.crt \
		--namespace $(NAMESPACE); \
	kubectl delete secret operator-ca-tls --namespace $(NAMESPACE) || true; \
	kubectl create secret generic operator-ca-tls \
   		--from-file=public.crt=scripts/minio/selfsigned.crt \
		--from-file=private.key=scripts/minio/selfsigned.key \
		--namespace $(NAMESPACE)