# -*- encoding: utf-8 -*-
"""
Processing of tags command
"""
import dateutil.parser

from ..consts import PER_PAGE
from ..libs.utils import readable_memory_format, print_result, digest_to_short
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


def formatted_image_info(repo):
    """ Return image meta info from response JSON """
    images_platform = []
    images_size = []
    images_digest = []
    if 'images' in repo:
        for image in repo['images']:
            images_platform.append(
                f"os:{image['os']}-({image['os_version'] or 'N/A'}" \
                f") arch:{image['architecture']}"
            )
            images_size.append(readable_memory_format(
                image['size'] / 1024))
            images_digest.append(digest_to_short(image['digest']))

    return "\n".join(images_platform), "\n".join(images_size), "\n".join(images_digest)


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

                # digest
                if 'digest' in repo:
                    digest = repo['digest']
                else:
                    digest = 'N/A'

                # Convert full_size in bytes to KB
                size_in_kb = repo['full_size'] / 1024
                formatted_size = readable_memory_format(size_in_kb)
                rows.append([repo['name'], formatted_size, formatted_date, digest_to_short(digest),
                             *formatted_image_info(repo)])
            header = ['Name', 'Size', 'Last updated', 'Digest', 'Images platform',
                      'Image size', 'Images digest']
            print_result(args.format, rows, header, resp['content']['count'],
                         args.page)
            total_pages = int(((resp['content']['count'] - 1) / per_page) + 1)
            return total_pages
        print('This repo has no tags')
        return None

    code = resp['code']
    print(f'Error {code} fetching tags for: {orgname}/{args.reponame}')
