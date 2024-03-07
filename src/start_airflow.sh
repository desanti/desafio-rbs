# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)

. .env

echo "Airflow Home: ${AIRFLOW_HOME}"

airflow standalone

# Visit localhost:8085 in the browser and use the admin account details
# shown on the terminal to login.
# Enable the example_bash_operator dag in the home page