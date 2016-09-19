# -*- encoding: utf-8 -*-
import sys
import argparse
import importlib
from os import path
from consts import *
from libs.utils import *
from libs.docker_client import DockerClient
from libs.docker_hub_client import DockerHubClient


class CondAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        x = kwargs.pop('to_be_required', [])
        super(CondAction, self).__init__(option_strings, dest, **kwargs)
        self.make_required = x

    def __call__(self, parser, namespace, values, option_string=None):
        for x in self.make_required:
            x.required = True
        try:
            setattr(namespace, self.dest, values)
            return super(CondAction, self).__call__(parser, namespace, values,
                                                    option_string)
        except NotImplementedError:
            pass


def main():
    parser = argparse.ArgumentParser(
        prog="docker-hub", description=DESCRIPTION, epilog=EPILOG,
             formatter_class=argparse.RawTextHelpFormatter)
    org_name_arg = parser.add_argument('--orgname', help=HELPMSGS['orgname'])
    parser.add_argument('method', type=str.lower, choices=VALID_METHODS,
                        nargs=1, help=HELPMSGS['method'], action=CondAction,
                        to_be_required=[org_name_arg])

    docker_client = DockerClient()
    docker_hub_client = DockerHubClient()
    if not docker_client.get_auth_token():
        if not docker_hub_client.get_token():
            username = None
            password = None
            while not username:
                username = user_input('Enter docker hub username: ')
            while not password:
                password = user_input('Enter docker hub password: ')

            if not docker_hub_client.login(username, password):
                print 'Error logging in to docker hub.'
                sys.exit(1)

    # Print help if no arguments given
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    command = importlib.import_module('src.commands.' + args.method)
    command.run(docker_hub_client, args.orgname)
