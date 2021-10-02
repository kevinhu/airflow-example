# airflow-example

Running:
1. Run `setup.sh`
2. Start DataHub with `datahub docker quickstart`
3. Start Postgres with `postgres -D /usr/local/var/postgres`
4. Start Redis with `redis-server /usr/local/etc/redis.conf`
5. Start Celery worker with `airflow celery worker`
6. Start scheduler with `poetry run airflow scheduler`
7. Start webserver with `poetry run airflow webserver --port 9000`