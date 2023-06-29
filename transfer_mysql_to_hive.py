from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from pyhive import hive


mysql_conn_id = 'your_mysql_connection'
mysql_table = 'your_mysql_table'


hive_conn_id = 'your_hive_connection'
hive_table = 'your_hive_table'


def transfer_mysql_to_hive():
    mysql_hook = MySqlHook(mysql_conn_id)
    hive_conn = hive.connect(hive_conn_id)
    

    mysql_conn = mysql_hook.get_conn()
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute(f"SELECT * FROM {mysql_table}")
    mysql_data = mysql_cursor.fetchall()
    

    hive_cursor = hive_conn.cursor()
    for row in mysql_data:
        hive_cursor.execute(f"INSERT INTO {hive_table} VALUES {row}")
    

    hive_conn.commit()
    hive_cursor.close()
    hive_conn.close()
    mysql_cursor.close()
    mysql_conn.close()


dag = DAG(
    dag_id='mysql_to_hive_transfer',
    start_date=datetime(2023, 6, 29),
    schedule_interval='@daily'
)


transfer_task = PythonOperator(
    task_id='transfer_task',
    python_callable=transfer_mysql_to_hive,
    dag=dag
)

