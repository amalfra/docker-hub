# -*- encoding: utf-8 -*-

import dateutil.parser

from ..libs.utils import *
from ..libs.config import Config


def run(docker_hub_client, args):
    """ The command to list tags for given repo on docker hub

        >>> from ..tests.docker_hub_client import \
            NoResultsTestingDockerHubClient, WithResultsTestingDockerHubClient
        >>> from collections import namedtuple
        >>> args = namedtuple('args', 'orgname reponame page format')
        >>> docker_hub_client = NoResultsTestingDockerHubClient()
        >>> run(docker_hub_client,
        ...     args(orgname='docker', reponame='docker', page='1',
        ...          format='json'))
        This repo has no tags
        >>> docker_hub_client = WithResultsTestingDockerHubClient()
        >>> run(docker_hub_client,
        ...     args(orgname='docker', reponame='docker', page='1',
        ...          format='json'))
        [
          {
            "Last updated": "2018-12-12 14:40",
            "Name": "1.4.2-alpine",
            "Size": "15.09 MB"
          }
        ]
    """
    config = Config()
    orgname = args.orgname or config.get('orgname')
    resp = docker_hub_client.get_tags(orgname, args.reponame, args.page)

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
            print('This repo has no tags')
    else:
        print('Error fetching tags for: {0}/{1}'.
              format(orgname, args.reponame))
