from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator


# No Dag at top level of module, has no effect on scheduler
def subdag_1(main_dag_name, subdag_name, start_date, schedule_interval):
    # you might like to make the name a parameter too
    dag = DAG(
        f"{main_dag_name}.{subdag_name}",
        # note the repetition here
        schedule_interval=schedule_interval,
        start_date=start_date,
        tags=["this_is_a_subdag"],
    )

    some_other_task_1 = BashOperator(
        bash_command="echo 'halfway there'", task_id="middle-1", dag=dag
    )

    some_other_task_2 = BashOperator(
        bash_command="echo 'halfway there'", task_id="middle-2", dag=dag
    )

    some_other_task_3 = BashOperator(
        bash_command="echo 'halfway there'", task_id="middle-3", dag=dag
    )

    return dag
