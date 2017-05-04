"""
A DAG docstring might be a good way to explain at a high level
what problem space the DAG is looking at.
Links to design documents, upstream dependencies etc
are highly recommended.
"""
import os
import pwd
from datetime import date, datetime, timedelta
from airflow.models import DAG  # Import the DAG class
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sqlite_operator import SQliteOperator
from airflow.operators.sensors import SqlSensor

d = date.today()


def get_username():
    return pwd.getpwuid(os.getuid())[0]


user = get_username()

default_args = {
    'owner': user,
    'depends_on_past': False,
    'start_date': datetime(d.year, d.month, d.day) - timedelta(days=7),
    'email': ['yourself@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'sqlite_example_dag_' + user.replace('.', ''),
    default_args=default_args,
    schedule_interval=timedelta(days=1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t0 = SqlSensor(
    task_id='check_babynames_tables',
    delta=timedelta(seconds=1),
    dag=dag)

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)


def my_cool_function(ds=None, **kwargs):
    print "{}".format(ds)


t2 = PythonOperator(
    task_id='show_ds',
    python_callable=my_cool_function,
    retries=3,
    provide_context=True,
    dag=dag)

# Airflow uses a templating language called Jinja
#

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated_task',
    bash_command=templated_command,
    params={'my_param': 'This is my parameter value'},
    dag=dag)

t1.set_upstream(t0)
t2.set_upstream(t1)
t3.set_upstream(t1)

t4 = SQliteOperator(
    'sqlite',
    sql='SELECT state, COUNT(1) FROM babynames GROUP BY state',
    sqlite_conn_id='babynames',
    dag=dag
)

t4.set_upstream(t3)
# deps = {
#     'wait_a_second': ['print_date'],
#     'print_date': ['show_ds'],
#     'show_ds': ['templated_task'],
# }

# for downstream, upstream_list in deps.items():
#     for upstream in upstream_list:
#         dag.set_dependency(upstream, downstream)
