from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import csv
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

# Path to the transformed CSV file
file_path = "/home/hajar/airflow/data/fixed_transformed_train.csv"

# Function to load data from CSV into PostgreSQL
def load_to_postgres():
    # Connect to PostgreSQL via Airflow Hook
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    # Create table in PostgreSQL if it does not exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS employee_dataa (
        Age INT,
        Attrition VARCHAR(50),
        BusinessTravel VARCHAR(50),
        Department VARCHAR(50),
        Education INT,
        EducationField VARCHAR(50),
        Gender VARCHAR(10),
        JobSatisfaction INT,
        MonthlyIncome FLOAT,
        NumCompaniesWorked INT,
        PercentSalaryHike FLOAT,
        PerformanceRating INT,
        RelationshipSatisfaction INT,
        TotalWorkingYears INT,
        TrainingTimesLastYear INT,
        YearsAtCompany INT,
        YearsInCurrentRole INT,
        YearsWithCurrManager INT
    );
    """
    cursor.execute(create_table_sql)
    
    # Insert data from CSV into the PostgreSQL table
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        insert_sql = """
        INSERT INTO employee_dataa (
            Age, Attrition, BusinessTravel, Department, Education, EducationField,
            Gender, JobSatisfaction, MonthlyIncome, NumCompaniesWorked,
            PercentSalaryHike, PerformanceRating, RelationshipSatisfaction,
            TotalWorkingYears, TrainingTimesLastYear, YearsAtCompany,
            YearsInCurrentRole, YearsWithCurrManager
        ) VALUES (
            %(Age)s, %(Attrition)s, %(BusinessTravel)s, %(Department)s,
            %(Education)s, %(EducationField)s, %(Gender)s, %(JobSatisfaction)s,
            %(MonthlyIncome)s, %(NumCompaniesWorked)s, %(PercentSalaryHike)s,
            %(PerformanceRating)s, %(RelationshipSatisfaction)s, %(TotalWorkingYears)s,
            %(TrainingTimesLastYear)s, %(YearsAtCompany)s, %(YearsInCurrentRole)s,
            %(YearsWithCurrManager)s
        )
        """
        
        for row in reader:
            # Convert data to match table column types if necessary
            row['Age'] = int(row['Age']) if row['Age'] else None
            row['MonthlyIncome'] = float(row['MonthlyIncome']) if row['MonthlyIncome'] else None
            # Add more conversions as needed
            
            cursor.execute(insert_sql, row)
    
    # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()

# Define the DAG
dag = DAG(
    'etl_postgres_load',
    description='ETL DAG to load transformed data into PostgreSQL',
    schedule_interval=None,  # No scheduling for now
    start_date=datetime(2024, 11, 8),
    catchup=False
)

# Define tasks
start = DummyOperator(
    task_id='start',
    dag=dag
)

load_data = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    dag=dag
)

# Tâche Bash pour exécuter spark-submit
spark_task = BashOperator(
    task_id='spark_test_task',
    bash_command='spark-submit /home/hajar/airflow/spark/spark_application.py',
    dag=dag
)

# Define task dependencies
start >> spark_task >> load_data
