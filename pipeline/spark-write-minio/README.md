# Spark on Kubernetes

```bash
docker build --progress=plain -f pipeline/spark-write-minio/Dockerfile pipeline/spark-write-minio -t spark-custom:3.5.3

k create secret generic minio-secret \
    --from-literal=AWS_ACCESS_KEY_ID=minio \
    --from-literal=AWS_SECRET_ACCESS_KEY=minio123 \
    --from-literal=ENDPOINT=https://myminio-hl.data-platform.svc.cluster.local:9000 \
    --from-literal=AWS_REGION=us-east-1 \
    --namespace data-platform


```