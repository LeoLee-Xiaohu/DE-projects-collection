from datetime import timedelta
from airflow import DAG 
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import detetime
from fm_artists_etl import run_fm_etl

default_args = {
    'owner' : "8893-leo",
    'depends_on_past':False ,
    'start_date': datetime(2021,8,1),
    'email':"leolikedata@gmail.com",
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag =DAG(
    'fm_dag',
    default_args = default_args,
    description = 'Ingest popular artists from Last FM API'
)

run_etl = PythonOperator(
    task_id = 'fmAPI_artists_etl',
    python_callable = run_fm_etl,
    dag = dag 
)