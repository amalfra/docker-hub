from ..libs.config import Config


def run(docker_hub_client, args):
    """ The command to list and modify config values """
    config = Config()
    all_config = config.get_all()
    for key in all_config:
        print("%s: %s" % (key, all_config[key]))
