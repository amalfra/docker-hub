# -*- encoding: utf-8 -*-
from ..libs.utils import *
from datetime import datetime


def run(docker_hub_client, args):
    """ The command to list repos of given org from docker hub """
    resp = docker_hub_client.get_repos(args.orgname)
    if resp['code'] == 200:
        if resp['content']['count'] > 0:
            rows = []
            for repo in resp['content']['results']:
                rows.append([repo['name'], repo['description'],
                            repo['star_count'], repo['pull_count']])
            header = ['Name', 'Description', 'Star count', 'Pull count']
            print_result(args.format, rows, header)
    else:
        print 'Error fetching repos for: ' + args.orgname
