# -*- encoding: utf-8 -*-
from .. import __version__


def run(docker_hub_client, args):
    """ The command to print current version """
    print('docker-hub ' + __version__)
