# -*- encoding: utf-8 -*-
"""
The entry point
"""
import sys
import argparse
import importlib
import os
from .consts import DESCRIPTION, EPILOG, HELPMSGS, VALID_METHODS, VALID_DISPLAY_FORMATS, \
    VALID_ACTIONS, NO_TIP_METHODS, NO_TIP_FORMATS, TIPS
from .libs.utils import CondAction
from .libs.docker_client import DockerClient
from .libs.docker_hub_client import DockerHubClient


def main():
    """ Start of execution """
    parser = argparse.ArgumentParser(
        prog="docker-hub", description=DESCRIPTION, epilog=EPILOG,
             formatter_class=argparse.RawTextHelpFormatter)
    username_arg = parser.add_argument('-u', '--username',
                                       help=HELPMSGS['username'])
    org_name_arg = parser.add_argument('-o', '--orgname',
                                       help=HELPMSGS['orgname'])
    org_name_arg.configName = 'orgname'
    repo_name_arg = parser.add_argument('-r', '--reponame',
                                        help=HELPMSGS['reponame'])
    parser.add_argument('-p', '--page', nargs='?', default=1,
                        help=HELPMSGS['page'])
    parser.add_argument('-a', '--all-pages', action='store_true',
                        help=HELPMSGS['all_pages'])
    parser.add_argument('-f', '--format', help=HELPMSGS['format'],
                        choices=VALID_DISPLAY_FORMATS)

    required_args = {
        'repos': [org_name_arg],
        'queue': [org_name_arg],
        'tags': [org_name_arg, repo_name_arg],
        'builds': [org_name_arg, repo_name_arg],
        'users': [username_arg]
    }
    parser.add_argument('method', type=str.lower, choices=VALID_METHODS,
                        nargs=1, help=HELPMSGS['method'], action=CondAction,
                        to_be_required=required_args)
    parser.add_argument('action', type=str.lower, choices=VALID_ACTIONS,
                        nargs='?', help=HELPMSGS['action'])
    parser.add_argument('param1', type=str.lower, nargs='?')
    parser.add_argument('param2', type=str.lower, nargs='?')

    # Print help if no arguments given
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    docker_client = DockerClient()
    docker_hub_client = DockerHubClient()
    # If Docker Hub username and password envs provided do login just for this
    # session, ie don't persist token in config
    docker_hub_username_env = os.getenv('DOCKER_HUB_USERNAME', None)
    docker_hub_password_env = os.getenv('DOCKER_HUB_PASSWORD', None)
    if docker_hub_username_env and docker_hub_password_env:
        if not docker_hub_client.login(docker_hub_username_env,
                                       docker_hub_password_env, False):
            print('Invalid credentials. Failed logging in to Docker Hub.')
            sys.exit(1)
    # Check if an auth token is present
    login_token_present = docker_client.get_auth_token() or \
        docker_hub_client.get_token()

    args = parser.parse_args()

    if args.all_pages and args.page != 1:
        print('You cannot use all_pages and page args together.')
        sys.exit(1)

    # Execute the command provided by user
    command = importlib.import_module('src.commands.' + args.method)
    command.run(docker_hub_client, args)

    if args.method not in NO_TIP_METHODS and args.format not in \
       NO_TIP_FORMATS and not login_token_present:
        print('\nTip: ' + TIPS[0])

if __name__ == '__main__':
    main()
