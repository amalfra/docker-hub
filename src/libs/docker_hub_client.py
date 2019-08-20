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

    def do_request(self, url, method='GET', data={}):
        valid_methods = ['GET', 'POST']
        if method not in valid_methods:
            raise ValueError('Invalid HTTP request method')
        headers = {'Content-type': 'application/json'}
        if self.auth_token:
            headers['Authorization'] = 'JWT ' + self.auth_token
        request_method = getattr(requests, method.lower())
        if len(data) > 0:
            data = json.dumps(data, indent=2, sort_keys=True)
            resp = request_method(url, data, headers=headers)
        else:
            resp = request_method(url, headers=headers)
        content = {}
        if resp.status_code == 200:
            content = json.loads(resp.content.decode())
        return {'content': content, 'code': resp.status_code}

    def login(self, username=None, password=None, save_config=True):
        data = {'username': username, 'password': password}
        self.auth_token = None
        resp = self.do_request(DOCKER_HUB_API_ENDPOINT + 'users/login/',
                               'POST', data)
        if resp['code'] == 200:
            self.auth_token = resp['content']['token']
            if save_config:
                self.config.set('auth_token', self.auth_token)
        return resp['code'] == 200

    def get_token(self):
        return self.auth_token

    def get_repos(self, org, page=1, per_page=PER_PAGE):
        url = '{0}repositories/{1}/?page={2}&page_size={3}'. \
               format(DOCKER_HUB_API_ENDPOINT, org, page, per_page)
        return self.do_request(url)

    def get_tags(self, org, repo, page=1, per_page=PER_PAGE):
        url = '{0}repositories/{1}/{2}/tags?page={3}&page_size={4}'. \
               format(DOCKER_HUB_API_ENDPOINT, org, repo, page, per_page)
        return self.do_request(url)

    def get_users(self, username):
        url = '{0}users/{1}'.format(DOCKER_HUB_API_ENDPOINT, username)
        return self.do_request(url)

    def get_buildhistory(self, org, repo, page=1, per_page=PER_PAGE):
        url = '{0}repositories/{1}/{2}/buildhistory?page={3}&page_size={4}'. \
                format(DOCKER_HUB_API_ENDPOINT, org, repo, page, per_page)
        return self.do_request(url)
