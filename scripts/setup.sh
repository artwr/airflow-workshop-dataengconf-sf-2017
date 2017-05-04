#!/bin/bash
set -eo pipefail
set -x

# From http://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "$SCRIPT_DIR"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

while [[ $# -gt 1 ]];
do
key="$1"

case $key in
    -y|--install_all)
    install_all="yes"
    echo "This option will install all"
    shift # past argument
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

# Defining helper functions
install_venvwrapper () {
    pip install --user virtualenvwrapper
    export WORKON_HOME=~/.virtualenvs
    mkdir -p $WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh
}
create_kernel () {
  if python -c "import jupyter"; then
    pip install ipykernel
    python -m ipykernel install --user --name=airflow_workshop_kernel
  else
    echo "Jupyter not present skipping kernel creation";
  fi
}
cleanup_airflow_home () {
  AIRFLOW_HOME="${REPO_DIR}/airflow/";
  rm -rf "$AIRFLOW_HOME"
}
setup_airflow () {
  export AIRFLOW_HOME=${REPO_DIR:=.}/airflow/
  mkdir -p $AIRFLOW_HOME/dags
  mkdir -p $AIRFLOW_HOME/logs
  airflow version
  airflow initdb
}

# Run all is
if [ -z ${install_all+x} ]; then
  echo "Upgrading pip and virtualenv"
  pip install --user --upgrade pip virtualenv
  echo "Installing Jupyter for the custom operator code lab"
  pip install --user jupyter
  echo "Create airflow_workshop virtualenv"
  install_venvwrapper
  rmvirtualenv airflow_workshop
  mkvirtualenv airflow_workshop
  workon airflow_workshop
  pip install airflow==1.8.0
  create_kernel
  echo "Setup Airflow"
  cleanup_airflow_home
  setup_airflow
  exit 0
fi

while true; do
    read -r -p "Do you wish to upgrade pip and virtualenv?" yn
    case $yn in
        [Yy]* ) pip install --user --upgrade pip virtualenv; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

while true; do
    read -r -p "Do you wish to install jupyter for the code lab?" yn1
    case $yn1 in
        [Yy]* ) pip install --user jupyter; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

while true; do
    read -r -p "Do you wish to setup Airflow for the workshop? (This will cleanup previous installs)" yn2
    case $yn2 in
        [Yy]* )
            echo "Create airflow_workshop virtualenv"
            install_venvwrapper
            rmvirtualenv airflow_workshop
            mkvirtualenv airflow_workshop
            workon airflow_workshop
            pip install airflow==1.8.0
            create_kernel
            echo "Setup Airflow"
            cleanup_airflow_home
            setup_airflow
            break
            ;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

