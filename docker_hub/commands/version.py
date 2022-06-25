# -*- encoding: utf-8 -*-
"""
Process version command
"""
from .. import __version__


def run():
    """ The command to print current version """
    print('docker-hub ' + __version__)
