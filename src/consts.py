# -*- encoding: utf-8 -*-
EPILOG = 'Docker Hub in your terminal'
DESCRIPTION = 'Access docker hub from your terminal'
HELPMSGS = {
 'method': 'The api method to query {%(choices)s}',
 'orgname': 'Your orgname',
 'format': 'You can dispaly results in %(choices)s formats',
 'page': 'The page of result to fetch'
}
VALID_METHODS = ['repos']
VALID_DISPLAY_FORMATS = ['table', 'json']
DOCKER_AUTH_FILE = '~/.docker/config.json'
CONFIG_FILE = '~/.docker-hub/config.json'
DOCKER_HUB_API_ENDPOINT = 'https://hub.docker.com/v2/'
PER_PAGE = 15
