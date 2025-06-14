# -*- encoding: utf-8 -*-
"""
Tests tags command
"""
import json
from collections import namedtuple

from src.commands.tags import run, formatted_image_info
from ..docker_hub_client import \
    NoResultsTestingDockerHubClient, WithTagsResultsTestingDockerHubClient
from ..helpers import convert_key_to_result_format, generate_tag_results


Args = namedtuple('args', 'orgname reponame page format all_pages')


def test_no_tags(capsys):
    """ When there are no tags returned by API """
    docker_hub_client = NoResultsTestingDockerHubClient()
    run(
        docker_hub_client,
        Args(
            orgname='docker', reponame='docker', page=1, format='json',
            all_pages=False
        )
    )

    captured = capsys.readouterr()
    assert captured.out == 'This repo has no tags\n'


def test_no_tags_and_all_pages(capsys):
    """ When all_page applied during no tags returned by API """
    docker_hub_client = NoResultsTestingDockerHubClient()
    run(
        docker_hub_client,
        Args(
            orgname='docker', reponame='docker', page=1, format='json',
            all_pages=True
        )
    )

    captured = capsys.readouterr()
    assert captured.out == 'This repo has no tags\n'


def test_with_tags(capsys):
    """ When there are tags returned by API """
    docker_hub_client = WithTagsResultsTestingDockerHubClient(12)
    run(
        docker_hub_client,
        Args(
            orgname='docker', reponame='docker', page=1, format='json',
            all_pages=False
        )
    )
    results = generate_tag_results(12)
    formatted_results = convert_key_to_result_format(results, {
        'last_updated': 'Last updated',
        'name': 'Name',
        'full_size': 'Size'
    })
    headers = ['Images platform', 'Image size', 'Images digest']
    for i, repo in enumerate(results):
        formatted_results[i]['Digest'] = repo['digest'] or 'N/A'
        for key, val in enumerate(formatted_image_info(repo)):
            formatted_results[i][headers[key]] = val

    captured = capsys.readouterr()
    assert json.loads(captured.out) == formatted_results


def test_with_tags_and_all_pages(capsys):
    """ When all_pages applied there are tags returned by API """
    docker_hub_client = WithTagsResultsTestingDockerHubClient(200)
    run(
        docker_hub_client,
        Args(
            orgname='docker', reponame='docker', page=1, format='json',
            all_pages=True
        )
    )
    results = generate_tag_results(200)
    formatted_results = convert_key_to_result_format(results, {
        'last_updated': 'Last updated',
        'name': 'Name',
        'full_size': 'Size'
    })
    headers = ['Images platform', 'Image size', 'Images digest']
    for i, repo in enumerate(results):
        formatted_results[i]['Digest'] = repo['digest'] or 'N/A'
        for key, val in enumerate(formatted_image_info(repo)):
            formatted_results[i][headers[key]] = val

    captured = capsys.readouterr()
    assert json.loads(captured.out) == formatted_results
