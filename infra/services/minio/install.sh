#!/bin/bash

set -e
set -x

helm upgrade --install --namespace data-platform \
    minio-operator infra/services/minio/operator

helm upgrade --install --namespace data-platform \
    minio-tenant infra/services/minio/tenant