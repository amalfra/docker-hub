# -*- encoding: utf-8 -*-
"""
Process config command
"""
from ..libs.utils import print_result
from ..libs.config import Config


def run(_, args):
    """ The command to list and modify config values """
    config = Config()
    header = ['Config', 'Value']

    if not args.action:
        all_config = config.get_all()
        print_result('table', all_config.items(), header, len(all_config),
                     zero_result_msg='No config values found')
    elif args.action == 'set':
        if not args.param1:
            print('Config name is required')
            return
        if args.param2:
            config.set(args.param1, args.param2)
        else:
            config.remove(args.param1)
    elif args.action == 'get':
        value = config.get(args.param1)
        if value:
            print(value)
        else:
            print('Config not found')
