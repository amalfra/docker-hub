# -*- encoding: utf-8 -*-
"""
Process version command
"""
from .. import __version__


def run(_docker_hub_client, _args):
    """ The command to print current version """
    print('docker-hub ' + __version__)
