# -*- encoding: utf-8 -*-
"""
Process login command
"""
from ..libs.utils import user_input


def run(docker_hub_client, _args):
    """ The command to do Docker Hub login """
    username = None
    password = None
    while not username:
        username = user_input('Enter docker hub username: ')
    while not password:
        password = user_input('Enter docker hub password: ', True)

    if not docker_hub_client.login(username, password):
        print('\nInvalid credentials. Failed logging in to Docker Hub.')
    else:
        print('\nLogin Succeeded\n')
