"""gdeploy is a CLI for managing Dockerized Django projects.
This module implements commands available from the gdeploy CLI for creating
projects.
"""


import click
from gdeploy.framework.cli.utils import CONTEXT_SETTINGS


# pylint: disable=missing-function-docstring
@click.group(context_settings=CONTEXT_SETTINGS, name="GDeploy")
def create_cli():  # pragma: no cover
    pass
