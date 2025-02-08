# data-platform

```bash
# Create Kubernetes namespace
k create namespace data-platform
```

## Install MinIO

```bash
# Install client
brew install minio/stable/mc

# Install server
./infra/services/minio/install.sh 

# Port forward for MinIO service and set up alias, & is to run it in background
k port-forward service/myminio-hl 9000 -n data-platform &

# Alias for Tenant service
mc alias set myminio https://localhost:9000 minio minio123 --insecure

# Create a bucket
mc mb myminio/mybucket --insecure

# Try upload some files to MinIO bucket
```