from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime

# Définir le DAG
dag = DAG(
    'spark_test_dag',
    description='Test DAG pour vérifier la connexion Spark avec Airflow',
    schedule_interval=None,  # Pas de planification, exécution manuelle
    start_date=datetime(2024, 11, 8),
    catchup=False
)

# Tâche de début (DummyOperator pour le début du DAG)
start = DummyOperator(
    task_id='start',
    dag=dag
)

# Tâche Bash pour exécuter spark-submit
spark_task = BashOperator(
    task_id='spark_test_task',
    bash_command='spark-submit /home/hajar/airflow/spark/spark_application.py',
    dag=dag
)

# Définir la dépendance des tâches
start >> spark_task
