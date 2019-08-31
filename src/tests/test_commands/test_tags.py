import json
from collections import namedtuple

from ..docker_hub_client import \
    NoResultsTestingDockerHubClient, WithResultsTestingDockerHubClient
from src.commands.tags import run
from ..helpers import convert_key_to_result_format, generate_results


args = namedtuple('args', 'orgname reponame page format all_pages')


def test_no_tags(capsys):
    docker_hub_client = NoResultsTestingDockerHubClient()
    run(
        docker_hub_client,
        args(
            orgname='docker', reponame='docker', page='1', format='json',
            all_pages=False
        )
    )

    captured = capsys.readouterr()
    assert captured.out == 'This repo has no tags\n'


def test_no_tags_and_all_pages(capsys):
    docker_hub_client = NoResultsTestingDockerHubClient()
    run(
        docker_hub_client,
        args(
            orgname='docker', reponame='docker', page='1', format='json',
            all_pages=True
        )
    )

    captured = capsys.readouterr()
    assert captured.out == 'This repo has no tags\n'


def test_with_tags(capsys):
    docker_hub_client = WithResultsTestingDockerHubClient(12)
    run(
        docker_hub_client,
        args(
            orgname='docker', reponame='docker', page='1', format='json',
            all_pages=False
        )
    )
    results = generate_results(12)
    formatted_results = convert_key_to_result_format(results, {
        'last_updated': 'Last updated',
        'name': 'Name',
        'full_size': 'Size'
    })

    captured = capsys.readouterr()
    assert json.loads(captured.out) == formatted_results


def test_with_tags_and_all_pages(capsys):
    docker_hub_client = WithResultsTestingDockerHubClient(200)
    run(
        docker_hub_client,
        args(
            orgname='docker', reponame='docker', page='1', format='json',
            all_pages=True
        )
    )
    results = generate_results(200)
    formatted_results = convert_key_to_result_format(results, {
        'last_updated': 'Last updated',
        'name': 'Name',
        'full_size': 'Size'
    })

    captured = capsys.readouterr()
    assert json.loads(captured.out) == formatted_results
