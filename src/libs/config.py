# -*- encoding: utf-8 -*-
import json
from os import path, makedirs
from ..consts import CONFIG_FILE


class Config:
    """ Simple management of JSON config file """
    def __init__(self):
        self.config_data = {}
        self.config_json_file = path.expanduser(CONFIG_FILE)
        if path.isfile(self.config_json_file):
            with open(self.config_json_file) as data_file:
                self.config_data = json.load(data_file)
        else:
            # Create config dir if it doesn't exist
            config_dir = path.dirname(self.config_json_file)
            if not path.isdir(config_dir):
                makedirs(config_dir)

            with open(self.config_json_file, 'w+') as data_file:
                data_file.write('{}')

    def get(self, key):
        if key in self.config_data:
            return self.config_data[key]
        return None

    def set(self, key, value=None):
        self.config_data[key] = value
        with open(self.config_json_file, 'w') as outfile:
            json.dump(self.config_data, outfile)
