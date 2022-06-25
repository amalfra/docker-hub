# -*- encoding: utf-8 -*-
"""
Tests users command
"""
import json
from collections import namedtuple

from src.commands.users import run
from ..docker_hub_client import \
    NoResultsUsersTestingDockerHubClient, WithUserResultsTestingDockerHubClient
from ..helpers import generate_results


Args = namedtuple('args', 'username page format all_pages')


def test_no_users(capsys):
    """ When there is no user profile found by API """
    docker_hub_client = NoResultsUsersTestingDockerHubClient()
    username = 'test'
    run(
        docker_hub_client,
        Args(
          username, page=1, format='json',
          all_pages=False
        )
    )

    captured = capsys.readouterr()
    assert captured.out == f'Error fetching profile for: {username}\n'

def test_no_users_and_all_pages(capsys):
    """ When all_page applied during no user found by API """
    docker_hub_client = NoResultsUsersTestingDockerHubClient()
    username = 'test'
    run(
        docker_hub_client,
        Args(
            username, page=1, format='json',
            all_pages=True
        )
    )

    captured = capsys.readouterr()
    assert captured.out == f'Error fetching profile for: {username}\n'

def test_with_users(capsys):
    """ When there is user returned API """
    docker_hub_client = WithUserResultsTestingDockerHubClient()
    username = 'test'
    run(
        docker_hub_client,
        Args(
            username, page=1, format='json',
            all_pages=False
        )
    )
    results = generate_results(1)

    captured = capsys.readouterr()
    assert json.loads(captured.out) == results

def test_with_users_and_all_pages(capsys):
    """ When all_pageas applied there is user returned API """
    docker_hub_client = WithUserResultsTestingDockerHubClient()
    username = 'test'
    run(
        docker_hub_client,
        Args(
            username, page=1, format='json',
            all_pages=True
        )
    )
    results = generate_results(1)

    captured = capsys.readouterr()
    assert json.loads(captured.out) == results
