# -*- encoding: utf-8 -*-
"""
Client for intereacting with Docker engine
"""
import json
from os import path
from ..consts import DOCKER_AUTH_FILE


#pylint: disable=too-few-public-methods
class DockerClient:
    """ A wrapper for communication with docker engine """
    def __init__(self):
        """ We load the docker engine config file when intialized """
        self.docker_config_data = {}
        config_json_file = path.expanduser(DOCKER_AUTH_FILE)
        if path.isfile(config_json_file):
            with open(config_json_file, encoding='UTF-8') as data_file:
                self.docker_config_data = json.load(data_file)

    def get_auth_token(self):
        """ Just get the auth token from docker config file """
        if 'auths' in self.docker_config_data:
            for auth in self.docker_config_data['auths']:
                if 'auth' in self.docker_config_data['auths'][auth]:
                    return self.docker_config_data['auths'][auth]['auth']

        return False
