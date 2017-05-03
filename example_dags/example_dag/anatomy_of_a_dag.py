"""
A DAG docstring might be a good way to explain at a high level
what problem space the DAG is looking at.
Links to design documents, upstream dependencies etc
are highly recommended.
"""
from datetime import datetime, timedelta
from airflow.models import DAG  # Import the DAG class
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import TimeDeltaSensor

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'start_date': datetime(2017, 4, 21),
    # You want an owner and possibly a team alias
    'email': ['yourteam@example.com', 'you@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'pool': 'default',
}

dag = DAG(
    dag_id='anatomy_of_a_dag',
    description="This describes my DAG",
    default_args=default_args,
    schedule_interval=timedelta(days=1))   # This is a daily DAG.

# t0, t1, t2 and t3 are examples of tasks created by instantiating operators
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

# Setting dependencies using task objects

t1.set_upstream(t0)
t2.set_upstream(t1)
t3.set_upstream(t1)

# Setting dependencies using task_id
# deps = {
#     'wait_a_second': ['print_date'],
#     'print_date': ['show_ds'],
#     'show_ds': ['templated_task'],
# }

# for downstream, upstream_list in deps.items():
#     for upstream in upstream_list:
#         dag.set_dependency(upstream, downstream)
