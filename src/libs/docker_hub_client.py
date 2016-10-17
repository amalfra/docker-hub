# -*- encoding: utf-8 -*-
import json
import requests
from ..consts import DOCKER_HUB_API_ENDPOINT, PER_PAGE
from .config import Config


class DockerHubClient:
    """ Wrapper to communicate with docker hub API """
    def __init__(self):
        self.config = Config()
        self.auth_token = self.config.get('auth_token')

    def do_get(self, url):
        headers = {'Content-type': 'application/json'}
        if self.auth_token:
            headers['Authorization'] = 'JWT ' + self.auth_token
        resp = requests.get(url, headers=headers)
        content = {}
        if resp.status_code == 200:
            content = json.loads(resp.content.decode())
        return {'content': content, 'code': resp.status_code}

    def do_post(self, url, data={}):
        data = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        if self.auth_token:
            headers['Authorization'] = 'JWT ' + self.auth_token
        resp = requests.post(url, data, headers=headers)
        content = {}
        if resp.status_code == 200:
            content = json.loads(resp.content.decode())
        return {'content': content, 'code': resp.status_code}

    def login(self, username=None, password=None):
        resp = self.do_post(DOCKER_HUB_API_ENDPOINT + 'users/login/',
                            {'username': username, 'password': password})
        if resp['code'] == 200:
            self.auth_token = resp['content']['token']
            self.config.set('auth_token', self.auth_token)
        return resp['code'] == 200

    def get_token(self):
        return self.auth_token

    def get_repos(self, org, page=1):
        url = DOCKER_HUB_API_ENDPOINT + 'repositories/' + org + '/?page=' \
         + str(page) + '&page_size=' + str(PER_PAGE)
        return self.do_get(url)
