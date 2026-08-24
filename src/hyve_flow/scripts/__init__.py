"""Standalone task scripts, shipped as files for deployment into task environments.

The modules here are not imported by the suite-building code; they are copied to
the execution host and run there, against that environment's own dependencies
(the ``scripts`` extra mirrors what they import). Locate them with
``importlib.resources.files("hyve_flow.scripts")``.
"""
