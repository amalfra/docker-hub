# -*- encoding: utf-8 -*-
from ..libs.utils import *


def run(docker_hub_client, orgname):
    resp = docker_hub_client.get_repos(orgname)
    if resp['code'] == 200:
        print_header('Found %s Repositories' % (resp['content']['count']))
        if resp['content']['count'] > 0:
            rows = []
            for repo in resp['content']['results']:
                rows.append([repo['name'], repo['description'],
                            repo['star_count'], repo['pull_count']])
            header = ['Name', 'Description', 'Star count', 'Pull count']
            print_table(header, rows)
    else:
        print 'Error fetching repos for: ' + orgname
