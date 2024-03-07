"""
### DESAFIO RBS

Faz a extração dos dados da API RandomUser e armazena no zona RAW

Faz o processamento dos dados e armazena na zona Curated

Faz a carga de dados para o zona APP

Todas as zonas estão em banco de dados Postgres.

"""

from datetime import datetime

from airflow.models import DAG
from airflow.operators.python import PythonOperator

from config.owners import owner
from projects.desafio_db.pipeline import ExtractUserToRaw, UserEventRawToCurated, UserCuratedToApplication


def create_task(
        task_id: str,
        callable_function: callable,
        trigger_rule: str = "all_success",
):
    return PythonOperator(
        task_id=f"{task_id}",
        python_callable=callable_function,
        trigger_rule=trigger_rule,
    )


default_args = {
    "owner": owner.name,
    "depends_on_past": False,
    "email": owner.email,
    "email_on_failure": False,
    "email_on_retry": False
}

with DAG(
        dag_id="desafio_db",
        default_args=default_args,
        start_date=datetime(2024, 3, 1),
        max_active_runs=1,
        schedule_interval=None,
        catchup=False,
        description="Desafio RBS utilizando banco de dados"
) as dag:
    dag.doc_md = __doc__

    extract_user_to_raw = create_task("extract_user_to_raw", ExtractUserToRaw.entrypoint)

    process_users_to_curated = create_task("process_users_to_curated", UserEventRawToCurated.entrypoint)

    load_users_to_app = create_task("load_users_to_app", UserCuratedToApplication.entrypoint)

    extract_user_to_raw >> process_users_to_curated >> load_users_to_app
