# -*- encoding: utf-8 -*-
"""
Process builds command
"""
import dateutil.parser
from ..libs.utils import print_result
from ..consts import BUILD_STATUS


def run(docker_hub_client, args):
    """ The command to list builds for given repo on docker hub """
    resp = docker_hub_client.get_buildhistory(args.orgname, args.reponame,
                                              args.page)
    if resp['code'] == 200:
        if resp['content']['count'] > 0:
            rows = []
            for repo in resp['content']['results']:
                name = repo['build_code']
                status = repo['status']
                tag = repo['dockertag_name']
                status = BUILD_STATUS.get(status, status)
                created_date = dateutil.parser.parse(repo['created_date'])
                created_date = created_date.strftime("%Y-%m-%d %H:%M")
                last_updated = dateutil.parser.parse(repo['last_updated'])
                last_updated = last_updated.strftime("%Y-%m-%d %H:%M")
                rows.append([name, tag, status, created_date, last_updated])
            header = ['Build', 'Tag', 'Status', 'Created', 'Last updated']
            print_result(args.format, rows, header, resp['content']['count'],
                         args.page)
    else:
        print(f'Error fetching builds for: {args.orgname}/{args.reponame}')
