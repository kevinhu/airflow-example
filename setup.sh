# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
export AIRFLOW_HOME=$(pwd)

AIRFLOW_VERSION=2.1.4
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.6
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.1.4/constraints-3.6.txt
poetry run pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# initialize the database
poetry run airflow db init

poetry run airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --password admin \
    --role Admin \
    --email admin@admin.org

# start the web server, default port is 8080
# poetry run airflow webserver --port 9000

# start the scheduler
# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
# poetry run airflow scheduler

# visit localhost:8080 in the browser and use the admin account you just
# created to login. Enable the example_bash_operator dag in the home page

# For Kafka-based (standard Kafka sink config can be passed via extras):
poetry run airflow connections add  --conn-type 'datahub_kafka' 'datahub_kafka_default' --conn-host 'broker:9092' --conn-extra '{}'
poetry run airflow connections add  --conn-type 'datahub_rest' 'datahub_rest_default' --conn-host 'http://localhost:8080'