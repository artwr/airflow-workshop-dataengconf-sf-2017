"""
A DAG docstring might be a good way to explain at a high level
what problem space the DAG is looking at.
Links to design documents, upstream dependencies etc
are highly recommended.
"""
from datetime import date, datetime, timedelta
from airflow.models import DAG  # Import the DAG class
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import TimeDeltaSensor

d = date.today()

default_args = {
    'owner': 'your_ldap',
    'depends_on_past': False,
    'start_date': datetime(d.year, d.month, d.day) - timedelta(days=7),
    'email': ['yourteam@airbnb.com', 'yourself@airbnb.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'default',    # 'default' or 'silver' or 'backfill'
}

dag = DAG(
    'DATAU302_example_dag',
    default_args=default_args,
    description="This will show up in the DAG view in the web UI",
    schedule_interval=timedelta(days=1))   # This is a daily DAG.

# t1, t2 and t3 are examples of tasks created by instantiating operators
t0 = TimeDeltaSensor(
    task_id='wait_a_second',
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


# deps = {
#     'wait_a_second': ['print_date'],
#     'print_date': ['show_ds'],
#     'show_ds': ['templated_task'],
# }

# for downstream, upstream_list in deps.items():
#     for upstream in upstream_list:
#         dag.set_dependency(upstream, downstream)
