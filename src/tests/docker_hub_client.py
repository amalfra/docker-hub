# -*- encoding: utf-8 -*-
import json
from ..libs.docker_hub_client import DockerHubClient


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
    def do_request(self, url, method='GET', data={}):
        content = {'count': 1, 'results': [{'last_updated': '2018-12-12 14:40',
                   'name': '1.4.2-alpine', 'full_size': 15820065}]}
        if 'login' in url:
            content = self._fake_login()
        return {'content': content, 'code': 200}
