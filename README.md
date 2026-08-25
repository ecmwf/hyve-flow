# Hyve Flow

Reusable [pyflow](https://github.com/ecmwf/pyflow) suite-building components for
hydrological verification workflows. The package is consumed as a library by suite
repositories such as `hyve-suites`, which import `hyve_flow` at suite-build time to
assemble ecFlow nodes and tasks.

## Development

The project uses [uv](https://docs.astral.sh/uv/) for dependency management. The
interpreter is pinned by `.python-version` and the resolved dependency set is committed
in `uv.lock`, so an environment can be reproduced with:

```shell
uv sync                 # core dependencies only
uv sync --all-extras    # plus test, dev and scripts extras
```

Run anything inside that environment with `uv run`:

```shell
uv run python -c "import hyve_flow; print(hyve_flow.__version__)"
uv run pytest
```

`uv lock` regenerates the lock file after changing dependencies in `pyproject.toml`.

### Running the tests

`pyflow` needs the `ecflow` Python bindings, which are not distributed on PyPI. Tests
that build pyflow nodes skip when the bindings are unavailable. At ECMWF they come from
the ecflow module, which sets `ECFLOW_DIR` for pyflow to discover:

```shell
module load ecflow
uv run pytest
```

### Installing without uv

For environments that already provide their own interpreter and dependencies (CI images,
conda environments), the standard editable install works too:

```shell
pip install -e .
```

## Dependencies and the task environment

The package declares two separate sets of dependencies, because two separate environments
are involved:

- **Required dependencies** (`pyflow-workflow-generator`, `pyflow-wellies`) are what
  `import hyve_flow` needs — the environment in which a suite definition is *built*.
- **The `scripts` extra** mirrors what the task scripts under `hyve_flow/scripts/` import
  (`xarray`, `earthkit-*`, `conflator`, `pydantic`, `hydro-verification`). It exists for
  working on those scripts locally; building a suite does not need it.

Those task scripts are deployed as files and run on the execution host, inside an
environment provisioned separately by the wellies tool store. `hyve_flow` is deliberately
*not* part of that environment, and so declares no console entry points — the scripts are
located as package data via `importlib.resources.files("hyve_flow.scripts")` rather than
installed as commands.
