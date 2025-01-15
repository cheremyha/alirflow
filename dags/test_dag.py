from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from sqlalchemy import text

from connections.hooks.clickhouse_hook import ClickHouseHook_wms

clickhouse_hook_wms = ClickHouseHook

# Настройки по умолчанию
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 1),
    'retries': 1,
}

# Создание DAG
dag = DAG(
    'test_dag_new',
    default_args=default_args,
    description='A simple test DAG with logging',
    schedule_interval='@daily',
    max_active_runs=100,
    concurrency=50,
)


def click_house():

    sql = """
       select

               *

       from sandbox.test
       where 1=1
       """

    df = clickhouse_hook_wms.get_pandas_df(
        sql=sql,
    )

    print(df.head())

    engine = clickhouse_hook_wms.get_alchemy_engine_wms()

    print('Successfully create an engine object')

    with engine.connect() as connection:
        print('Successfully created session with engine object')
        connection.execute(text("SET ROLE sandbox_engineer"))
        # Insert data using to_sql method from Pandas.
        df.to_sql(
            schema='sandbox',
            name='test',
            index=False,
            if_exists="append",
            con=connection
        )

        print(f'Successfully Insert Data to Table using df.to_sql, with {len(df)} rows')

click_house = PythonOperator(
    task_id='click_house_task',
    python_callable=click_house,
    dag=dag,
)


click_house