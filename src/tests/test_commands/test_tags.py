import json
from collections import namedtuple

from ..docker_hub_client import \
    NoResultsTestingDockerHubClient, WithResultsTestingDockerHubClient

from src.commands.tags import run


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


def test_with_tags(capsys):
    docker_hub_client = WithResultsTestingDockerHubClient()

    run(
        docker_hub_client,
        args(
            orgname='docker', reponame='docker', page='1', format='json',
            all_pages=False
        )
    )

    captured = capsys.readouterr()
    assert json.loads(captured.out) == [
        {
            "Last updated": "2018-12-12 14:40",
            "Name": "1.4.2-alpine",
            "Size": "15.09 MB"
        }
    ]
