import sys  # Import sys module
import os  # Import os module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.scraper import scrape_jobs
from scripts.database import store_jobs
from scripts.analysis import analyze_jobs
from scripts.visualization import visualize_jobs


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    dag_id='job_market_analysis',
    default_args=default_args,
    description='A DAG for analyzing job market trends',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    scrape = PythonOperator(
        task_id='scrape_jobs',
        python_callable=scrape_jobs,
    )

    store = PythonOperator(
        task_id='store_jobs',
        python_callable=store_jobs,
    )

    analyze = PythonOperator(
        task_id='analyze_jobs',
        python_callable=analyze_jobs,
    )

    visualize = PythonOperator(
        task_id='visualize_jobs',
        python_callable=visualize_jobs,
    )

    scrape >> store >> analyze >> visualize
