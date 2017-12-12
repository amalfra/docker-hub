# -*- encoding: utf-8 -*-
from ..libs.utils import *
from ..consts import BUILD_STATUS
import dateutil.parser


def repo_history(docker_hub_client, args):
    """ Get repo history
    """
    resp = docker_hub_client.get_buildhistory(
            args.orgname, args.reponame, args.page)
    if not resp['code'] == 200:
        return
    if not resp['content']['results']:
        return
    for history in resp['content']['results']:
        if not args.all:
            if history['status'] == 10:
                return
            if history['status'] < 0:
                return
        yield history


def repos(docker_hub_client, args):
    """ Generate valid repos
    """
    if args.reponame:
        for history in repo_history(docker_hub_client, args):
            yield args.reponame, history
        return

    for page in range(1, 100):
        resp = docker_hub_client.get_repos(args.orgname, page, per_page=100)
        if not resp['code'] == 200:
            return

        for repo in resp['content']['results']:
            if not repo['is_automated']:
                continue
            args.reponame = repo['name']
            for history in repo_history(docker_hub_client, args):
                yield args.reponame, history


def run(docker_hub_client, args):
    """ The command to list repos of given org from docker hub """
    rows = []
    count = 0
    for name, history in repos(docker_hub_client, args):
        count += 1
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
