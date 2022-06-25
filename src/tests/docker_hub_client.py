# -*- encoding: utf-8 -*-
"""
Tests for Dockerhub API client
"""
from src.libs.docker_hub_client import DockerHubClient
from .helpers import generate_results


class BaseTestingDockerHubClient(DockerHubClient):
    """ Fake wrapper to simulate communication with docker hub API """
    def _fake_login(self):
        return {'token': 'random-token'}


class NoResultsTestingDockerHubClient(BaseTestingDockerHubClient):
    """ When API returns no results """
    def do_request(self, url, method='GET', data=None):
        content = {'count': 0}
        if 'login' in url:
            content = self._fake_login()
        return {'content': content, 'code': 200}

class NoResultsUsersTestingDockerHubClient(BaseTestingDockerHubClient):
    """ When API returns no results for users endpoint """
    def do_request(self, url, method='GET', data=None):
        return {'content': None, 'code': 404}

class WithResultsTestingDockerHubClient(BaseTestingDockerHubClient):
    """ When API returns results """
    def __init__(self, results_count=1):
        super().__init__()
        self.results_count = results_count

    def do_request(self, url, method='GET', data=None):
        content = {'count': 1, 'results': generate_results(self.results_count)}
        if 'login' in url:
            content = self._fake_login()
        return {'content': content, 'code': 200}

class WithUserResultsTestingDockerHubClient(BaseTestingDockerHubClient):
    """ When API returns user result """
    def do_request(self, url, method='GET', data=None):
        content = generate_results(1)[0]
        if 'login' in url:
            content = self._fake_login()
        return {'content': content, 'code': 200}
