"""Lineage Backend
An example DAG demonstrating the usage of DataHub's Airflow lineage backend.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.example_dags.subdags.subdag import subdag
from airflow.utils.dates import days_ago

from airflow.utils.trigger_rule import TriggerRule

from airflow.operators.subdag import SubDagOperator
from airflow.operators.dummy import DummyOperator

from subdag import subdag_1


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


# def load_subdag(parent_dag_name, child_dag_name, start_date, schedule_interval, args):
#     dag_subdag = DAG(
#         dag_id=f"{parent_dag_name}.{child_dag_name}",
#         default_args=args,
#         schedule_interval=schedule_interval,
#         start_date=start_date,
#     )
#     with dag_subdag:
#         for i in range(5):
#             t = BashOperator(
#                 task_id=f"load_subdag_{i}",
#                 bash_command=f"echo '{i}'",
#                 default_args=args,
#                 dag=dag_subdag,
#             )

#     return dag_subdag


with DAG(
    DAG_NAME,
    default_args=default_args,
    description="An example DAG demonstrating the usage of DataHub's Airflow lineage backend.",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2019,1,1),
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

    section_1 = SubDagOperator(
        task_id="section-1",
        subdag=subdag_1(DAG_NAME, "section-1", dag.start_date, dag.schedule_interval),
        trigger_rule=TriggerRule.ALL_DONE
    )

    some_other_task = BashOperator(
        bash_command="echo 'halfway there'",
        task_id="middle",
    )

    section_2 = SubDagOperator(
        task_id="section-2",
        subdag=subdag_1(DAG_NAME, "section-2", dag.start_date, dag.schedule_interval),
        trigger_rule=TriggerRule.ALL_DONE
    )

    end = BashOperator(
        bash_command="echo 'done!'",
        task_id="end",
        outlets={"datasets": [Dataset("snowflake", "mydb.schema.tableC")]},
    )

    start >> section_1 >> some_other_task >> section_2 >> end
