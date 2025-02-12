from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def print_hello():
    print("Hello, World!")

with DAG(
    dag_id="print_every_5_seconds",
    schedule="@every_5s",  # Run every 5 seconds
    start_date=days_ago(2),
    catchup=False,
    dagrun_timeout=pendulum.duration(minutes=1), # Timeout for the entire DAG run
    tags=["example"],
) as dag:
    print_hello_task = PythonOperator(
        task_id="print_hello",
        python_callable=print_hello,
        provide_context=True, 
    )