# -*- encoding: utf-8 -*-
from .. import __version__


def run(docker_hub_client, args):
    """ The command to list repos of given org from docker hub """
    print('docker-hub ' + __version__)
