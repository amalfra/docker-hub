# -*- encoding: utf-8 -*-
"""
Client to communicate with Dockerhub REST API
"""
import json
import requests
from ..consts import DOCKER_HUB_API_ENDPOINT, PER_PAGE
from .config import Config


class DockerHubClient:
    """ Wrapper to communicate with docker hub API """
    def __init__(self):
        self.config = Config()
        self.auth_token = self.config.get('auth_token')

    def do_request(self, url, method='GET', data=None):
        """ Does HTTP request """
        valid_methods = ['GET', 'POST']
        if method not in valid_methods:
            raise ValueError('Invalid HTTP request method')
        headers = {'Content-type': 'application/json'}
        if self.auth_token:
            headers['Authorization'] = 'JWT ' + self.auth_token
        request_method = getattr(requests, method.lower())
        if data and len(data) > 0:
            data = json.dumps(data, indent=2, sort_keys=True)
            resp = request_method(url, data, headers=headers)
        else:
            resp = request_method(url, headers=headers)
        content = {}
        if resp.status_code == 200:
            content = json.loads(resp.content.decode())
        return {'content': content, 'code': resp.status_code}

    def login(self, username=None, password=None, save_config=True):
        """ Do login to Dockerhub. Get's token which is saved in config file """
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
        """ Fetch auth token """
        return self.auth_token

    def get_repos(self, org, page=1, per_page=PER_PAGE):
        """ Get all repositories of an organization """
        url = f'{DOCKER_HUB_API_ENDPOINT}repositories/{org}/?page={page}&page_size={per_page}'
        return self.do_request(url)

    def get_tags(self, org, repo, page=1, per_page=PER_PAGE):
        """ Get all tags of an repository """
        url = f'{DOCKER_HUB_API_ENDPOINT}repositories/{org}/{repo}' \
            + f'/tags?page={page}&page_size={per_page}'
        return self.do_request(url)

    def get_users(self, username):
        """ Get user profile info """
        url = f'{DOCKER_HUB_API_ENDPOINT}users/{username}'
        return self.do_request(url)

    def get_buildhistory(self, org, repo, page=1, per_page=PER_PAGE):
        """ Get build history of a repository """
        url = f'{DOCKER_HUB_API_ENDPOINT}repositories/{org}/{repo}' \
            + f'/buildhistory?page={page}&page_size={per_page}'
        return self.do_request(url)
