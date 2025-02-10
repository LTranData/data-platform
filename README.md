# data-platform

```bash
# Create Kubernetes namespace
k create namespace data-platform
```

## Install MinIO

```bash
# Add repository
helm repo add minio-operator https://operator.min.io
helm search repo minio-operator
helm repo update

# Install client
brew install minio/stable/mc

# Download operator config
curl -sLo infra/services/minio/operator/values.yaml https://raw.githubusercontent.com/minio/operator/master/helm/operator/values.yaml

# Download tenant config
curl -sLo infra/services/minio/tenant/values.yaml https://raw.githubusercontent.com/minio/operator/master/helm/tenant/values.yaml

# Install server
make -f scripts/minio/Makefile install

# Port forward for MinIO service and set up alias, & is to run it in background
k port-forward service/myminio-hl 9000 -n data-platform &
k port-forward service/myminio-console 9443 -n data-platform &

# Alias for Tenant service
mc alias set myminio https://localhost:9000 minio minio123 --insecure

# Create a bucket
mc mb myminio/mybucket --insecure

# Try upload some files to MinIO bucket
# CA certificate in pod: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
# sudo keytool -importcert -alias MinIO_Cert -file ca.crt -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit
```

## Install Spark cluster

```bash
# Add repository
helm repo add spark-operator https://kubeflow.github.io/spark-operator
helm search repo spark-operator
helm repo update

# Download Spark config
curl -sLo infra/services/spark/values.yaml https://raw.githubusercontent.com/kubeflow/spark-operator/refs/heads/master/charts/spark-operator-chart/values.yaml

make -f scripts/spark/Makefile install
```