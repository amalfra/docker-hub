# -*- encoding: utf-8 -*-
from ..libs.utils import *
import dateutil.parser


def run(docker_hub_client, args):
    """ The command to user profile from docker hub """
    resp = docker_hub_client.get_users(args.username)
    if resp['code'] == 200:
        rows = []
        for key in resp['content']:
            if key == 'date_joined':
                formatted_date = dateutil.parser \
                                  .parse(resp['content'][key])
                formatted_date = formatted_date.strftime("%Y-%m-%d %H:%M")
                resp['content'][key] = formatted_date
            rows.append([key, resp['content'][key]])
        heading = "User profile of %s" % (args.username)
        print_result(args.format, rows, heading=heading)
    else:
        print('Error fetching profile for: ' + args.username)
