# -*- encoding: utf-8 -*-
import json
from os import path
from ..consts import *


class DockerClient:
    def __init__(self):
        self.docker_config_data = {}
        config_json_file = path.expanduser(DOCKER_AUTH_FILE)
        if path.isfile(config_json_file):
            with open(config_json_file) as data_file:
                self.docker_config_data = json.load(data_file)

    def get_auth_token(self):
        if self.docker_config_data['auths']:
            for auth in self.docker_config_data['auths']:
                if self.docker_config_data['auths'][auth]['auth']:
                    return self.docker_config_data['auths'][auth]['auth']

        return False
