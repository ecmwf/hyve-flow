"""Shared fixtures for the hyve-flow test suite.

``pyflow`` needs the ``ecflow`` Python bindings, which are not distributed on
PyPI. At ECMWF they come from the ecflow module, which sets ``ECFLOW_DIR`` for
pyflow to discover::

    module load ecflow
    uv run pytest

Tests that build pyflow nodes skip when those bindings are absent.
"""

import pytest


@pytest.fixture
def tools():
    """Stand-in for a wellies ``ToolStore``.

    ``ReanalysisProcessing`` only ever calls ``load()`` on it, so a stub keeps
    the tests free of a real tool store and its configuration.
    """

    class ToolStoreStub:
        def load(self, exec_env):
            return f"# load tools for {exec_env}"

    return ToolStoreStub()


@pytest.fixture
def config_script():
    """Stand-in for the caller-supplied config writer.

    Records the keyword arguments it was called with so tests can assert on the
    contract between ``build_extraction_task`` and its caller.
    """

    class ConfigScript:
        def __init__(self):
            self.calls = []

        def __call__(self, **kwargs):
            self.calls.append(kwargs)
            return ["# write extract.yaml"]

    return ConfigScript()


@pytest.fixture
def processing(tools):
    """A ``ReanalysisProcessing`` wired to the stub tool store."""
    reanalysis = pytest.importorskip(
        "hyve_flow.reanalysis",
        reason="pyflow needs the ecflow bindings; run `module load ecflow` first",
        # pyflow raises a plain ImportError, not ModuleNotFoundError, when it
        # cannot locate the ecflow bindings.
        exc_type=ImportError,
    )
    return reanalysis.ReanalysisProcessing(
        config={"station_extraction": {"stations": "outlets.nc"}},
        tools=tools,
        exec_env="hpc",
    )
