# -*- encoding: utf-8 -*-
import dateutil.parser

from ..libs.utils import *
from ..libs.config import Config


def run(docker_hub_client, args):
    """ The command to list repos of given org from docker hub """
    config = Config()
    orgname = args.orgname or config.get('orgname')
    resp = docker_hub_client.get_repos(orgname, args.page)

    if resp['code'] == 200:
        if resp['content']['count'] > 0:
            rows = []
            for repo in resp['content']['results']:
                formatted_date = ''
                if repo['last_updated']:
                    formatted_date = \
                        dateutil.parser.parse(repo['last_updated'])
                    formatted_date = formatted_date.strftime("%Y-%m-%d %H:%M")
                rows.append([repo['name'], repo['description'],
                            repo['star_count'], repo['pull_count'],
                            formatted_date])
            header = ['Name', 'Description', 'Star count', 'Pull count',
                      'Last updated']
            print_result(args.format, rows, header, resp['content']['count'],
                         args.page)
    else:
        print('Error fetching repos for: ' + orgname)
