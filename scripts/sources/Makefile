# Makefile for source systems

NAMESPACE ?= data-platform
POSTGRES_OPERATOR ?= bitnami/postgresql

# Optional targets for specific components
.PHONY: install-postgres uninstall-postgres

install-postgres:
	@set -ex; \
	helm upgrade --install --namespace $(NAMESPACE) \
		postgres-source $(POSTGRES_OPERATOR) \
		--set global.postgresql.auth.postgresPassword=postgres \
		--set global.postgresql.auth.database=postgres

uninstall-postgres:
	@set -ex; \
	helm uninstall --namespace $(NAMESPACE) \
		postgres-source