import pendulum

from airflow.models.dag import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator

with DAG(
    dag_id="spark-write-minio",
    schedule=None,
    start_date=days_ago(2),
    catchup=False,
    dagrun_timeout=pendulum.duration(minutes=1),
    tags=["spark-write-minio"],
    template_searchpath=Variable.get("template_searchpath")
) as dag:
    spark_job = SparkKubernetesOperator(
        task_id='spark-job',
        application_file=f'{Variable.get("template_searchpath")}/spark/spark-write-minio.yaml',
        namespace="data-platform"
    )