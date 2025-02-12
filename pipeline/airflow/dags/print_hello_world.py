import pendulum

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

def print_hello():
    print("Hello, World!")

with DAG(
    dag_id="print_every_5_seconds",
    schedule=timedelta(seconds=5),  # Use timedelta for 5-second interval
    start_date=days_ago(2),
    catchup=False,
    dagrun_timeout=pendulum.duration(minutes=1),
    tags=["example"],
) as dag:
    print_hello_task = PythonOperator(
        task_id="print_hello",
        python_callable=print_hello,
        provide_context=True,
    )