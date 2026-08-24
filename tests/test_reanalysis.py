"""Unit tests for ``ReanalysisProcessing.build_extraction_task``."""

import pytest

pf = pytest.importorskip(
    "pyflow",
    reason="pyflow needs the ecflow bindings; run `module load ecflow` first",
    # pyflow raises a plain ImportError, not ModuleNotFoundError, when it cannot
    # locate the ecflow bindings.
    exc_type=ImportError,
)


class TestTaskAttributes:
    def test_returns_a_pyflow_task(self, processing, config_script):
        task = processing.build_extraction_task(config_script, task_args={})

        assert isinstance(task, pf.Task)

    def test_name_defaults_to_extract_stations(self, processing, config_script):
        task = processing.build_extraction_task(config_script, task_args={})

        assert task.name == "extract_stations"

    def test_explicit_name_is_respected(self, processing, config_script):
        task = processing.build_extraction_task(
            config_script, task_args={"name": "extract_glofas"}
        )

        assert task.name == "extract_glofas"

    def test_workdir_variable_comes_from_work_dir(self, processing, config_script):
        task = processing.build_extraction_task(
            config_script, task_args={}, work_dir="/scratch/run"
        )

        variables = {v.name: v.value for v in task.variables}
        assert variables["WORKDIR"] == "/scratch/run"


class TestConfigScriptContract:
    def test_receives_the_station_extraction_section(self, processing, config_script):
        processing.build_extraction_task(
            config_script, task_args={}, work_dir="/scratch/run"
        )

        assert config_script.calls == [
            {
                "config": {"stations": "outlets.nc"},
                "output_file": "extract.yaml",
                "work_dir": "/scratch/run",
            }
        ]

    def test_missing_section_passes_none(self, tools, config_script):
        from hyve_flow.reanalysis import ReanalysisProcessing

        processing = ReanalysisProcessing(config={}, tools=tools, exec_env="hpc")
        processing.build_extraction_task(config_script, task_args={})

        assert config_script.calls[0]["config"] is None


class TestScriptContents:
    def test_body_runs_the_extraction_in_the_work_directory(
        self, processing, config_script
    ):
        task = processing.build_extraction_task(config_script, task_args={})

        script = task.script.value
        assert "mkdir -p $WORKDIR" in script
        assert "cd $WORKDIR" in script
        assert "hyve-extract-timeseries extract.yaml" in script

    def test_tools_are_loaded_before_anything_else(self, processing, config_script):
        task = processing.build_extraction_task(
            config_script, task_args={}, preprocess="# preprocess"
        )

        script = task.script.value
        assert script.index("# load tools for hpc") < script.index(
            "# write extract.yaml"
        )
        assert script.index("# write extract.yaml") < script.index("# preprocess")
        assert script.index("# preprocess") < script.index("mkdir -p $WORKDIR")

    def test_preprocess_accepts_a_bare_string(self, processing, config_script):
        task = processing.build_extraction_task(
            config_script, task_args={}, preprocess="# single line"
        )

        assert "# single line" in task.script.value

    def test_preprocess_accepts_a_list(self, processing, config_script):
        task = processing.build_extraction_task(
            config_script, task_args={}, preprocess=["# first", "# second"]
        )

        script = task.script.value
        assert "# first" in script
        assert script.index("# first") < script.index("# second")

    def test_preprocess_defaults_to_nothing(self, processing, config_script):
        task = processing.build_extraction_task(config_script, task_args={})

        script = task.script.value
        assert script.index("# load tools for hpc") < script.index("mkdir -p $WORKDIR")
