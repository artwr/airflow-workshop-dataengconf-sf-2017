
Anatomy of a DAG
================

This tutorial walks you through some of the fundamental Airflow concepts,
objects, and their usage while writing your first pipeline.

Example Pipeline definition
---------------------------

Here is an example of a basic pipeline definition. Do not worry if this looks
complicated, a line by line explanation follows below.

.. code:: python

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


It's a DAG definition file
--------------------------

One thing to wrap your head around (it may not be very intuitive for everyone
at first) is that this Airflow Python script is really
just a configuration file specifying the DAG's structure as code.
The actual tasks defined here will run in a different context from
the context of this script. Different tasks run on different workers
at different points in time, which means that this script cannot be used
to cross communicate between tasks. Note that for this
purpose we have a more advanced feature called ``XCom``.

People sometimes think of the DAG definition file as a place where they
can do some actual data processing - that is not the case at all!
The script's purpose is to define a DAG object. It needs to evaluate
quickly (seconds, not minutes) since the scheduler will execute it
periodically to reflect the changes if any.


Importing Modules
-----------------

An Airflow pipeline is just a Python script that happens to define an
Airflow DAG object. Let's start by importing the libraries we will need.

.. code:: python

    # Import other librabries
    from datetime import datetime, timedelta
    # Import the DAG class
    from airflow.models import DAG
    # Import Operators.
    from airflow.operators.bash_operator import BashOperator
    from airflow.operators.python_operator import PythonOperator
    from airflow.operators.sensors import TimeDeltaSensor

Default Arguments
-----------------
We're about to create a DAG and some tasks, and we have the choice to
explicitly pass a set of arguments to each task's constructor
(which would become redundant), or (better!) we can define a dictionary
of default parameters that we can use when creating tasks.

.. code:: python

    from datetime import datetime, timedelta

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

For more information about the BaseOperator's parameters and what they do,
refer to the ``airflow.models.BaseOperator`` documentation.

Also, note that you could easily define different sets of arguments that
would serve different purposes. An example of that would be to have
different settings between a production and development environment.


Instantiate a DAG
-----------------

We'll need a DAG object to nest our tasks into. Here we pass a string
that defines the ``dag_id``, which serves as a unique identifier for your DAG.
We also pass the default argument dictionary that we just defined and
define a ``schedule_interval`` of 1 day for the DAG.

.. code:: python

    dag = DAG(
    dag_id='anatomy_of_a_dag',
    description="This describes my DAG",
    default_args=default_args,
    schedule_interval=timedelta(days=1))   # This is a daily DAG.

Tasks
-----
Tasks are generated when instantiating operator objects. An object
instantiated from an operator is called a constructor. The first argument
``task_id`` acts as a unique identifier for the task.

.. code:: python

    t0 = TimeDeltaSensor(
        task_id='wait_a_second',
        delta=timedelta(seconds=1),
        dag=dag)

    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
        dag=dag)

Notice how we pass a mix of operator specific arguments (``bash_command``) and
an argument common to all operators (``retries``) inherited
from BaseOperator to the operator's constructor. This is simpler than
passing every argument for every constructor call. Also, notice that in
the second task we override the ``retries`` parameter with ``3``.

The precedence rules for a task are as follows:

1.  Explicitly passed arguments
2.  Values that exist in the ``default_args`` dictionary
3.  The operator's default value, if one exists

A task must include or inherit the arguments ``task_id`` and ``owner``,
otherwise Airflow will raise an exception.

Templating with Jinja
---------------------
Airflow leverages the power of
`Jinja Templating <http://jinja.pocoo.org/docs/dev/>`_  and provides
the pipeline author
with a set of built-in parameters and macros. Airflow also provides
hooks for the pipeline author to define their own parameters, macros and
templates.

This tutorial barely scratches the surface of what you can do with
templating in Airflow, but the goal of this section is to let you know
this feature exists, get you familiar with double curly brackets, and
point to the most common template variable: ``{{ ds }}``.

.. code:: python

    templated_command = """
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7) }}"
            echo "{{ params.my_param }}"
        {% endfor %}
    """

    t3 = BashOperator(
        task_id='templated',
        bash_command=templated_command,
        params={'my_param': 'Parameter I passed in'},
        dag=dag)

Notice that the ``templated_command`` contains code logic in ``{% %}`` blocks,
references parameters like ``{{ ds }}``, calls a function as in
``{{ macros.ds_add(ds, 7)}}``, and references a user-defined parameter
in ``{{ params.my_param }}``.

The ``params`` hook in ``BaseOperator`` allows you to pass a dictionary of
parameters and/or objects to your templates. Please take the time
to understand how the parameter ``my_param`` makes it through to the template.

PythonOperator
--------------

The ``PythonOperator`` can execute an arbitrary Python callable (usually a function). The provide context flag can be useful if you want your function to be passed the Jinja context variables like ``ds``. In this case you can either add the parameter you want to your function signature, and add ``**kwargs`` to store the other parameters.

.. code:: python

    def my_cool_function(ds=None, **kwargs):
    print "{}".format(ds)


    t2 = PythonOperator(
        task_id='show_ds',
        python_callable=my_cool_function,
        retries=3,
        provide_context=True,
        dag=dag)


Separating Workflow definition and task definition
--------------------------------------------------

Files can also be passed to the ``bash_command`` argument, like
``bash_command='templated_command.sh'``, where the file location is relative to
the directory containing the pipeline file (``anatomy_of_a_dag.py`` in this case). This
may be desirable for many reasons, like separating your script's logic and
pipeline code, allowing for proper code highlighting in files composed in
different languages, and general flexibility in structuring pipelines. It is
also possible to define your ``template_searchpath`` as pointing to any folder
locations in the DAG constructor call.

For more information on the variables and macros that can be referenced
in templates, make sure to read through the :ref:`macros` section

Setting up Dependencies
-----------------------
We have two simple tasks that do not depend on each other. Here's a few ways
you can define dependencies between them:

.. code:: python

    t2.set_upstream(t1)

    # This means that t2 will depend on t1
    # running successfully to run
    # It is equivalent to
    # t1.set_downstream(t2)

    t3.set_upstream(t1)

    # all of this is equivalent to
    # dag.set_dependency('print_date', 'show_ds')
    # dag.set_dependency('print_date', 'templated')

Note that when executing your script, Airflow will raise exceptions when
it finds cycles in your DAG or when a dependency is referenced more
than once.

Recap
-----
Alright, so we have a pretty basic DAG. At this point your code should look
something like this:

.. code:: python

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

Testing
--------

Running the Script
''''''''''''''''''

Time to run some tests. First let's make sure that the pipeline
parses. Let's assume we're saving the code from the previous step in
``anatomy_of_a_dag.py`` in the DAGs folder referenced in your ``airflow.cfg``.
The default location for your DAGs is ``~/airflow/dags``.

.. code-block:: bash

    python ~/airflow/dags/anatomy_of_a_dag.py

If the script does not raise an exception it means that you haven't done
anything horribly wrong, and that your Airflow environment is somewhat
sound.

Command Line Metadata Validation
'''''''''''''''''''''''''''''''''
Let's run a few commands to validate this script further.

.. code-block:: bash

    # print the list of active DAGs
    airflow list_dags

    # prints the list of tasks the "anatomy_of_a_dag" dag_id
    airflow list_tasks anatomy_of_a_dag

    # prints the hierarchy of tasks in the anatomy_of_a_dag DAG
    airflow list_tasks anatomy_of_a_dag --tree


Testing
'''''''
Let's test by running the actual task instances on a specific date. The
date specified in this context is an ``execution_date``, which simulates the
scheduler running your task or dag at a specific date + time:

.. code-block:: bash

    # command layout: command subcommand dag_id task_id date

    # testing print_date
    airflow test anatomy_of_a_dag print_date 2015-06-01

    # testing sleep
    airflow test anatomy_of_a_dag show_ds 2015-06-01

Now remember what we did with templating earlier? See how this template
gets rendered and executed by running this command:

.. code-block:: bash

    # testing templated
    airflow test anatomy_of_a_dag templated 2015-06-01

This should result in displaying a verbose log of events and ultimately
running your bash command and printing the result.

Note that the ``airflow test`` command runs task instances locally, outputs
their log to stdout (on screen), doesn't bother with dependencies, and
doesn't communicate state (running, success, failed, ...) to the database.
It simply allows testing a single task instance.


Backfill
''''''''
Everything looks like it's running fine so let's run a backfill.
``backfill`` will respect your dependencies, emit logs into files and talk to
the database to record status. If you do have a webserver up, you'll be able
to track the progress. ``airflow webserver`` will start a web server if you
are interested in tracking the progress visually as your backfill progresses.

Note that if you use ``depends_on_past=True``, individual task instances
will depend on the success of the preceding task instance, except for the
start_date specified itself, for which this dependency is disregarded.

The date range in this context is a ``start_date`` and optionally an ``end_date``,
which are used to populate the run schedule with task instances from this dag.

.. code-block:: bash

    # optional, start a web server in debug mode in the background
    # airflow webserver --debug &

    # start your backfill on a date range
    airflow backfill anatomy_of_a_dag -s 2015-06-01 -e 2015-06-07

What's Next?
-------------
That's it, you've written, tested and backfilled your very first Airflow
pipeline. Merging your code into a code repository that has a master scheduler
running against it should get it to get triggered and run every day.

Here's a few things you might want to do next:

* Take an in-depth tour of the UI - click all the things!
* Keep reading the docs! Especially the sections on:

    * Command line interface
    * Operators
    * Macros

* Write your first pipeline!
