# airflow-example

Before running any commands, make sure `export AIRFLOW_HOME=$(pwd)` is run from the root of this repo. Alternatively, add the path of this repo to your `.zshrc` or similar.

Running:
1. Run `setup.sh`
2. Start DataHub with `datahub docker quickstart`
3. Start Postgres with `postgres -D /usr/local/var/postgres`
4. Start Redis with `redis-server /usr/local/etc/redis.conf`
5. Start Celery worker with `airflow celery worker`
6. Start scheduler with `poetry run airflow scheduler`
7. Start webserver with `poetry run airflow webserver --port 9000`

Note: the workers have a bit of a delay for subdags, so wait a minute or two for them to finish running when datahub_subdag is run.