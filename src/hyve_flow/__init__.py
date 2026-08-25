from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("hyve-flow")
except PackageNotFoundError:  # not installed, e.g. running from a source tree
    __version__ = "0.0.0"

__all__ = ["__version__"]
