"""The package is importable under its underscored name once installed."""

import hyve_flow


def test_package_is_importable():
    assert hyve_flow.__name__ == "hyve_flow"


def test_version_is_populated():
    assert isinstance(hyve_flow.__version__, str)
    assert hyve_flow.__version__
