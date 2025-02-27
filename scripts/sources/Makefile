# Makefile for source systems

NAMESPACE ?= data-platform
POSTGRES_OPERATOR ?= bitnami/postgresql

# Optional targets for specific components
.PHONY: install-postgres uninstall-postgres

install-postgres:
	@set -ex; \
	kubectl delete configmap postgresql-conf --namespace $(NAMESPACE) || true; \
	kubectl create configmap postgresql-conf \
		--from-file=postgresql.conf=scripts/sources/postgresql.conf \
		--namespace $(NAMESPACE); \
	helm upgrade --install --namespace $(NAMESPACE) \
		postgres-source $(POSTGRES_OPERATOR) \
		--set global.postgresql.auth.postgresPassword=postgres \
		--set global.postgresql.auth.database=postgres \
		--set primary.existingConfigmap=postgresql-conf

uninstall-postgres:
	@set -ex; \
	helm uninstall --namespace $(NAMESPACE) \
		postgres-source