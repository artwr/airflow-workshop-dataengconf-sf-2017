Setup your machine for the workshop
===================================

What you should have
--------------------

Your machine should have the following installed :
* Python (>2.7.10 at least for Python 2 or >3.4 for Python 3). If you are on OSX, installing homebrew and the homebrew python is highly recommended as well.
* SQLite (It should be installed on most systems)
* Upgrading pip is recommended.

  .. code-block:: bash

      pip install --user --upgrade pip


Automated setup
---------------

A script is provided to install most dependencies in this. Simply run scripts/setup.sh located `here <https://github.com/artwr/airflow-workshop-dataengconf-sf-2017/blob/master/scripts/setup.sh>`_ from the root of this git repository.


Manual Setup
------------

Get Juyter and virtualenv
'''''''''''''''''''''''''

I would recommend installing jupyter and virtualenv for testing.

.. code-block:: bash

    pip install -U --user virtualenv jupyter


Virtualenvwrapper
'''''''''''''''''

For ease of use I recommend virtualenvwrapper, but this is completely optional.

.. code-block:: bash

    pip install --user virtualenvwrapper
    export WORKON_HOME=~/.virtualenvs
    mkdir -p $WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh
    rmvirtualenv airflow_workshop
    mkvirtualenv airflow_workshop

Virtualenv
''''''''''

.. code-block:: bash

    rm -rf airflow_workshop
    virtualenv airflow_workshop
    source airflow_workshop/bin/activate

Installing Airflow
''''''''''''''''''
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

The current list of `extras` is available `here <https://github.com/apache/incubator-airflow/blob/master/setup.py#L249-L289>`_ and an older version can be found in the `docs <https://airflow.incubator.apache.org/installation.html#extra-packages>`_
