# -*- encoding: utf-8 -*-
import dateutil.parser

from ..consts import PER_PAGE
from ..libs.utils import *
from ..libs.config import Config


def run(docker_hub_client, args):
    """ The command to list tags for given repo on docker hub
    """
    config = Config()
    orgname = args.orgname or config.get('orgname')

    if args.all_pages:
        while not get_tags(docker_hub_client, orgname, args, per_page=100):
            args.page += 1
    else:
        get_tags(docker_hub_client, orgname, args)


def get_tags(docker_hub_client, orgname, args, per_page=PER_PAGE):
    resp = docker_hub_client.get_tags(
        orgname, args.reponame, args.page, per_page=per_page
    )
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
        print('Error {0} fetching tags for: {1}/{2}'.
              format(resp['code'], orgname, args.reponame))
        return resp['code']
