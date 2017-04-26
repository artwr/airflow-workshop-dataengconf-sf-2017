Installing Airflow
------------------

Preparing your machine
''''''''''''''''''''''

I would recommend installing jupyter and virtualenv for testing.

.. code-block:: bash

    pip install virtualenv jupyter

For ease of use, I recommend virtualenvwrapper.

.. code-block:: bash

    pip install virtualenvwrapper
    export WORKON_HOME=~/.virtualenvs
    mkdir -p $WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh

We should create a virtualenv for the class


.. code-block:: bash

    mkvirtualenv airflow_workshop


Getting Airflow
'''''''''''''''

The easiest way to install the latest stable version of Airflow is with ``pip``:

.. code-block:: bash

    pip install airflow

The current stable version is ``1.8.0``. You can install this version specifically by using

.. code-block:: bash

    pip install airflow==1.8.0

As Airflow is still currently evolving a decent amount, I recommend pinning the version
you use, if you do not feel like living on the bleeding edge.

You can also install Airflow with support for extra features like ``s3`` or ``mysql``:

.. code-block:: bash

    #Install the latest with extras
    pip install airflow[s3,mysql]
    #Install the 1.8.0 with specific extras
    pip install airflow[s3,mysql]==1.8.0

Note that this will only install the Python packages needed to talk to some external systems, but not these systems (MySQL needs to be installed separately by your method of choice.)

The full list of `extras` is available `here <https://github.com/apache/incubator-airflow/blob/master/setup.py#L249-L289>`_


For the workshop
''''''''''''''''

.. code-block:: bash

    #This should give you most of what you will need.
    pip install -r reqs/airflowenv_requirements.txt







