# -*- encoding: utf-8 -*-
import sys
import argparse
import importlib
from os import path
from .consts import *
from .libs.utils import *
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
    repo_name_arg = parser.add_argument('-r', '--reponame',
                                        help=HELPMSGS['reponame'])
    page = parser.add_argument('-p', '--page', nargs='?', default=1,
                               help=HELPMSGS['page'])
    display_format = parser.add_argument('-f', '--format',
                                         help=HELPMSGS['format'],
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

    # Print help if no arguments given
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    docker_client = DockerClient()
    docker_hub_client = DockerHubClient()
    # Check if an auth token is present
    login_token_present = docker_client.get_auth_token() or \
        docker_hub_client.get_token()

    args = parser.parse_args()
    # Execute the command provided by user
    command = importlib.import_module('src.commands.' + args.method)
    command.run(docker_hub_client, args)

    if args.method not in NO_TIP_METHODS and not login_token_present:
        print('\nTip: ' + TIPS[0])
