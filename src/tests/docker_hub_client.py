# -*- encoding: utf-8 -*-
import json
from ..libs.docker_hub_client import DockerHubClient


class TestingDockerHubClient(DockerHubClient):
    """ Fake wrapper to simulate communication with docker hub API """

    def _fake_login(self):
        return {'token': 'random-token'}

    def do_request(self, url, method='GET', data={}):
        content = {'count': 0}
        if 'login' in url:
            content = self._fake_login()
        return {'content': content, 'code': 200}
