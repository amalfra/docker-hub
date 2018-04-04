# -*- encoding: utf-8 -*-
from ..libs.utils import *
import dateutil.parser


def run(docker_hub_client, args):
    """ The command to list tags for given repo on docker hub

        >>> from ..tests.docker_hub_client import TestingDockerHubClient
        >>> from collections import namedtuple
        >>> args = namedtuple('args', 'orgname reponame page')
        >>> docker_hub_client = TestingDockerHubClient()
        >>> run(docker_hub_client,
        ...     args(orgname='docker', reponame='docker', page='1'))
    """
    resp = docker_hub_client.get_tags(args.orgname, args.reponame, args.page)
    if resp['code'] == 200:
        if resp['content']['count'] > 0:
            rows = []
            for repo in resp['content']['results']:
                formatted_date = ''
                if repo['last_updated']:
                    formatted_date = dateutil.parser \
                                      .parse(repo['last_updated'])
                    formatted_date = formatted_date.strftime("%Y-%m-%d %H:%M")
                # Convert full_size in bytes to KB
                size_in_kb = repo['full_size'] / 1024
                formatted_size = readableMemoryFormat(size_in_kb)
                rows.append([repo['name'], formatted_size, formatted_date])
            header = ['Name', 'Size', 'Last updated']
            print_result(args.format, rows, header, resp['content']['count'],
                         args.page)
    else:
        print('Error fetching tags for: {0}/{1}'.
              format(args.orgname, args.reponame))
