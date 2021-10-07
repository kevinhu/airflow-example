"""Lineage Backend
An example DAG demonstrating the usage of DataHub's Airflow lineage backend.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.subdag import SubDagOperator
from airflow.utils.trigger_rule import TriggerRule
from subdag import subdag

try:
    from airflow.operators.bash import BashOperator
except ModuleNotFoundError:
    from airflow.operators.bash_operator import BashOperator

from datahub_provider.entities import Dataset

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["jdoe@example.com"],
    "email_on_failure": False,
    "execution_timeout": timedelta(minutes=5),
}

DAG_NAME = "datahub_subdag"


with DAG(
    DAG_NAME,
    default_args=default_args,
    description="An example DAG demonstrating the usage of DataHub's Airflow lineage backend.",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2019, 1, 1),
    tags=["example_tag"],
    catchup=False,
) as dag:

    start = DummyOperator(
        inlets={
            "datasets": [
                Dataset("snowflake", "mydb.schema.tableA"),
                Dataset("snowflake", "mydb.schema.tableB"),
            ],
        },
        task_id="start",
    )

    subdag_1 = SubDagOperator(
        task_id="subdag-1",
        subdag=subdag(DAG_NAME, "subdag-1", dag.start_date, dag.schedule_interval),
        trigger_rule=TriggerRule.ALL_DONE,
    )

    some_other_task = BashOperator(
        bash_command="echo 'halfway there'",
        task_id="middle",
    )

    subdag_2 = SubDagOperator(
        task_id="subdag-2",
        subdag=subdag(DAG_NAME, "subdag-2", dag.start_date, dag.schedule_interval),
        trigger_rule=TriggerRule.ALL_DONE,
    )

    end = BashOperator(
        bash_command="echo 'done!'",
        task_id="end",
        outlets={"datasets": [Dataset("snowflake", "mydb.schema.tableC")]},
    )

    start >> subdag_1 >> some_other_task >> subdag_2 >> end
