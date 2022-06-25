# -*- encoding: utf-8 -*-
"""
Process users command
"""
import dateutil.parser
from ..libs.utils import print_result


def run(docker_hub_client, args):
    """ The command to user profile from docker hub """
    resp = docker_hub_client.get_users(args.username)
    if resp['code'] == 200:
        rows = [[]] if args.format == 'json' else []
        header = []
        for key in resp['content']:
            if key == 'date_joined':
                formatted_date = dateutil.parser \
                                  .parse(resp['content'][key])
                formatted_date = formatted_date.strftime("%Y-%m-%d %H:%M")
                resp['content'][key] = formatted_date
            if args.format == 'json':
                rows[0].append(resp['content'][key])
                header.append(key)
            else:
                rows.append([key, resp['content'][key]])
        heading = f'User profile of {args.username}'
        print_result(args.format, rows, header, heading=heading, count=1)
    else:
        print('Error fetching profile for: ' + args.username)
