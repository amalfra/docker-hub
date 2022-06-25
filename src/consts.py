# -*- encoding: utf-8 -*-
"""
This file contains all global config constants used by the app
"""
EPILOG = 'Docker Hub in your terminal'
DESCRIPTION = 'Access docker hub from your terminal'
HELPMSGS = {
 'method': 'The api method to query {%(choices)s}',
 'orgname': 'Your orgname',
 'reponame': 'The name of repository',
 'username': 'The Docker Hub username',
 'format': 'You can dispaly results in %(choices)s formats',
 'page': 'The page of result to fetch',
 'all_pages': 'Fetch all pages',
 'status': 'To query for only builds with specified status',
 'login': 'Authenticate with Docker Hub',
 'config': 'Manage configuration values',
 'action': 'Action to perform on an api method',
}
VALID_METHODS = ['repos', 'tags', 'builds', 'users', 'queue', 'version',
                 'login', 'config']
VALID_ACTIONS = ['set', 'get']
VALID_CONFIG_NAMES = ['orgname']
NO_TIP_METHODS = ['login', 'version', 'config']
NO_TIP_FORMATS = ['json']
VALID_DISPLAY_FORMATS = ['table', 'json']
DOCKER_AUTH_FILE = '~/.docker/config.json'
CONFIG_FILE = '~/.docker-hub/config.json'
DOCKER_HUB_API_ENDPOINT = 'https://hub.docker.com/v2/'
PER_PAGE = 15
SECURE_CONFIG_KEYS = ['auth_token']

BUILD_STATUS = {
    -4: 'canceled',
    -2: 'exception',
    -1: 'error',
    0: 'pending',
    1: 'claimed',
    2: 'started',
    3: 'cloned',
    4: 'readme',
    5: 'dockerfile',
    6: 'built',
    7: 'bundled',
    8: 'uploaded',
    9: 'pushed',
    10: 'done'
}

TIPS = [
    'You are not authenticated with Docker Hub. Hence only public \
resources will be fetched. Try authenticating using `docker login` or \
`docker-hub login` command to see more.'
]
