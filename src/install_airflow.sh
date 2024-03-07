
echo "---------------- INSTALANDO O AIRFLOW ------------------------"

. .env

AIRFLOW_REQUIREMENTS="requirements.txt"

# Install Airflow using the constraints file
AIRFLOW_VERSION="$(cat ${AIRFLOW_REQUIREMENTS} | grep "apache-airflow\[.*\]" | cut -d = -f 3)"
# For example: 2.2.5

PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.6

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-3.6.txt

echo "Versão do Airflow: ${AIRFLOW_VERSION}"
echo "Versão do Python:  ${PYTHON_VERSION}"
echo "Airflow Home: ${AIRFLOW_HOME}"

pip install -r ${AIRFLOW_REQUIREMENTS} --constraint "${CONSTRAINT_URL}"

# The Standalone command will initialise the database, make a user,
# and start all components for you.

airflow standalone
