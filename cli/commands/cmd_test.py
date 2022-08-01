import os
import subprocess

import click


@click.command()
@click.argument('path', default=os.path.join('flowstate', 'tests'))
def cli(path):
    """ Run tests with Pytest. """
    cmd = 'py.test {0}'.format(path)
    return subprocess.call(cmd, shell=True)
