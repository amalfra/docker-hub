# -*- encoding: utf-8 -*-
"""
Processing of tags command
"""
import dateutil.parser

from ..consts import PER_PAGE
from ..libs.utils import readable_memory_format, print_result
from ..libs.config import Config


def run(docker_hub_client, args):
    """ The command to list tags for given repo on docker hub
    """
    config = Config()
    orgname = args.orgname or config.get('orgname')

    if args.all_pages:
        resp = get_tags(docker_hub_client, orgname, args)
        while resp and resp > args.page:
            args.page += 1
            resp = get_tags(docker_hub_client, orgname, args)
    else:
        get_tags(docker_hub_client, orgname, args)


#pylint: disable=inconsistent-return-statements
def get_tags(docker_hub_client, orgname, args, per_page=PER_PAGE):
    """ Fetch tags of repository """
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
                formatted_size = readable_memory_format(size_in_kb)
                rows.append([repo['name'], formatted_size, formatted_date])
            header = ['Name', 'Size', 'Last updated']
            print_result(args.format, rows, header, resp['content']['count'],
                         args.page)
            total_pages = int(((resp['content']['count'] - 1)/per_page) + 1)
            return total_pages
        print('This repo has no tags')
        return None

    code = resp['code']
    print(f'Error {code} fetching tags for: {orgname}/{args.reponame}')
