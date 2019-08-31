# -*- encoding: utf-8 -*-
import json
from ..libs.docker_hub_client import DockerHubClient
from .helpers import generate_results


class BaseTestingDockerHubClient(DockerHubClient):
    """ Fake wrapper to simulate communication with docker hub API """

    def _fake_login(self):
        return {'token': 'random-token'}


class NoResultsTestingDockerHubClient(BaseTestingDockerHubClient):
    def do_request(self, url, method='GET', data={}):
        content = {'count': 0}
        if 'login' in url:
            content = self._fake_login()
        return {'content': content, 'code': 200}


class WithResultsTestingDockerHubClient(BaseTestingDockerHubClient):
    def __init__(self, results_count=1):
        self.results_count = results_count

    def do_request(self, url, method='GET', data={}):
        content = {'count': 1, 'results': generate_results(self.results_count)}
        if 'login' in url:
            content = self._fake_login()
        return {'content': content, 'code': 200}
