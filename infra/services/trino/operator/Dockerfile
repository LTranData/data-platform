FROM trinodb/trino:470

COPY scripts/minio/selfsigned.crt /etc/pki/ca-trust/source/anchors/
USER root
RUN update-ca-trust extract

USER trino