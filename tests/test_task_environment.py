"""hyve-flow builds task scripts; it must never be a dependency of one.

The generated tasks run in an environment provisioned by the wellies tool store
on the execution host. This package is a suite-build-time library only, so
nothing it emits may install or import it.
"""

import pytest

pytest.importorskip(
    "pyflow",
    reason="pyflow needs the ecflow bindings; run `module load ecflow` first",
    # pyflow raises a plain ImportError, not ModuleNotFoundError, when it cannot
    # locate the ecflow bindings.
    exc_type=ImportError,
)


@pytest.mark.parametrize("forbidden", ["hyve_flow", "hyve-flow", "pip install"])
def test_generated_script_does_not_reference_this_package(processing, config_script, forbidden):
    task = processing.build_extraction_task(config_script, task_args={}, preprocess=["# preprocess"])

    assert forbidden not in task.script.value


def test_task_environment_comes_from_the_tool_store(processing, config_script):
    """The only environment setup is whatever the tool store emits."""
    task = processing.build_extraction_task(config_script, task_args={})

    assert "# load tools for hpc" in task.script.value
