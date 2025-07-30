import importlib

import weave
from weave.integrations.patcher import SymbolPatcher, MultiPatcher
from weave.trace.autopatch import AutopatchSettings, IntegrationSettings
from pydantic import Field


inspect_patcher = MultiPatcher(
    [
        SymbolPatcher(
            lambda: importlib.import_module("inspect_ai._eval.run"),
            "task_run",
            weave.op(name="inspect_task"),
        )
    ]
)

def get_inspect_patcher(settings: IntegrationSettings | None = None) -> MultiPatcher:
    return inspect_patcher