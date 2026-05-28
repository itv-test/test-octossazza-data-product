import pytest
from pytest_mock.plugin import MockerFixture
from airflow import DAG
from airflow.models import DagBag
from airflow.models.variable import Variable
from airflow.utils.db import initdb


@pytest.fixture(scope="session")
def dag_bag() -> DagBag:
    initdb()
    return DagBag(
        dag_folder="marketing/test_octossazza",
        include_examples=False,
        safe_mode=True,
        read_dags_from_db=False,
        load_op_links=False,
    )


@pytest.fixture(scope="function")
def dag(dag_bag: DagBag) -> DAG:
    return dag_bag.get_dag("test_octossazza_dag")


@pytest.fixture(scope="function", autouse=True)
def airflow_vars(mocker: MockerFixture) -> None:
    mock_airflow_env_vars = {
        "platform-environment": "test",
        "platform-marketing-project-id": "itv-data-marketing-dom-test",
        "platform-region": "europe-west2",
    }
    mock_var_get = mocker.patch.object(Variable, "get")
    mock_var_get.side_effect = (
        lambda *args, **kwargs: mock_airflow_env_vars.get(args[0])
    )
