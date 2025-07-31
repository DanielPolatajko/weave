import pytest
import weave
from inspect_ai import task, Task, eval
from inspect_ai.solver import generate
from inspect_ai.scorer import exact
from inspect_ai.dataset import Sample
from weave.integrations.inspect import get_inspect_patcher
from pathlib import Path

@pytest.fixture(scope="function")
def patch_inspect():
    get_inspect_patcher().attempt_patch()

    yield

    get_inspect_patcher().undo_patch()


@pytest.mark.skip_clickhouse_client
@pytest.mark.vcr(
    filter_headers=["authorization"],
    allowed_hosts=["api.wandb.ai", "localhost"],
)
def test_inspect_quickstart(
    client: weave.trace.weave_client.WeaveClient,
    patch_inspect: None,
    tmp_path: Path,
) -> None:
    @task
    def hello_world():
        return Task(
            dataset=[
                Sample(
                    input="Just reply with Hello World",
                    target="Hello World",
                )
            ],
            solver=[generate()],
            scorer=exact(),
            metadata={"test": "test"}
        )

    eval(hello_world, model="mockllm/model", log_dir=str(tmp_path))

    calls = list(client.calls())
    assert len(calls) == 1
    assert "inspect_task" in calls[0]._op_name
