# -*- encoding: utf-8 -*-
EPILOG = 'Docker Hub in your terminal'
DESCRIPTION = 'Access docker hub from your terminal'
HELPMSGS = {
 'method': 'The api method to query {%(choices)s}',
 'orgname': 'Your orgname'
}
VALID_METHODS = ['repos']
DOCKER_AUTH_FILE = '~/.docker/config.json'
CONFIG_FILE = '~/.docker-hub/config.json'
DOCKER_HUB_API_ENDPOINT = 'https://hub.docker.com/v2/'
