# -*- encoding: utf-8 -*-
"""
Process queue command
"""
import dateutil.parser
from ..libs.utils import print_result
from ..consts import BUILD_STATUS


def repos(docker_hub_client, args):
    """ Generate valid repos """
    for page in range(1, 100):
        resp = docker_hub_client.get_repos(args.orgname, page, per_page=100)
        if not resp['code'] == 200:
            break
        for repo in resp['content']['results']:
            if repo['is_automated']:
                resp = docker_hub_client.get_buildhistory(
                        args.orgname, repo['name'])
                if not resp['code'] == 200:
                    continue
                if not resp['content']['results']:
                    continue
                for history in resp['content']['results']:
                    if history['status'] == 10:
                        break
                    if history['status'] < 0:
                        break
                    yield repo, history


def run(docker_hub_client, args):
    """ The command to list repos of given org from docker hub """
    rows = []
    count = 0
    for repo, history in repos(docker_hub_client, args):
        count += 1
        name = repo['name']
        tag = history['dockertag_name']
        status = history['status']
        status = BUILD_STATUS.get(status, status)
        created_date = dateutil.parser.parse(history['created_date'])
        created_date = created_date.strftime("%Y-%m-%d %H:%M")
        last_updated = dateutil.parser.parse(history['last_updated'])
        last_updated = last_updated.strftime("%Y-%m-%d %H:%M")
        rows.append([name, tag, status, created_date, last_updated])
    header = ['Name', 'Tag', 'Status', 'Created', 'Last updated']
    print_result(args.format, rows, header, count, args.page)
