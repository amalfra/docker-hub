# -*- encoding: utf-8 -*-
"""
Deals with config file
"""
import json
from os import path, makedirs
from ..consts import CONFIG_FILE, SECURE_CONFIG_KEYS, VALID_CONFIG_NAMES


class Config:
    """ Simple management of JSON config file """
    def __init__(self):
        self.config_data = {}
        self.config_json_file = path.expanduser(CONFIG_FILE)
        if path.isfile(self.config_json_file):
            with open(self.config_json_file, encoding='UTF-8') as data_file:
                self.config_data = json.load(data_file)
        else:
            # Create config dir if it doesn't exist
            config_dir = path.dirname(self.config_json_file)
            if not path.isdir(config_dir):
                makedirs(config_dir)

            with open(self.config_json_file, 'w+', encoding='UTF-8') as data_file:
                data_file.write('{}')

    def get(self, key):
        """ Fetch config from file """
        if key in self.config_data:
            return self.config_data[key]
        return None

    def set(self, key, value=None):
        """ Save config to file """
        if key not in VALID_CONFIG_NAMES and key not in SECURE_CONFIG_KEYS:
            print(key + ' is not a valid config name')
            return
        self.config_data[key] = value
        with open(self.config_json_file, 'w', encoding='UTF-8') as outfile:
            json.dump(self.config_data, outfile)

    def remove(self, key):
        """ Delete config from file """
        if key in self.config_data:
            self.config_data.pop(key)
        with open(self.config_json_file, 'w', encoding='UTF-8') as outfile:
            json.dump(self.config_data, outfile)

    def get_all(self):
        """ Get all config from file """
        return {k: self.config_data[k]
                for k in self.config_data if k not in SECURE_CONFIG_KEYS}
