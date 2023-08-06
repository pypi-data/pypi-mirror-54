import json
import os.path

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "default.json")


def load_json_file(path):
    with open(path) as json_file:
        json_dict = json.load(json_file)
    return json_dict


class Config:
    def __init__(self):
        self._config = self.default

    def __getitem__(self, key):
        return self._config[key]

    def update(self, custom_config=None):
        self._config.update(custom_config)

    @property
    def default(self):
        default_config_path = DEFAULT_CONFIG_PATH
        default_config = load_json_file(default_config_path)
        return default_config

    def load(self, path):
        custom_config = load_json_file(path)
        self.update(custom_config)

    def spacecraft_from_alias(self, alias):
        alias = alias.lower()
        for sc_key, sc_config in self._config["SPACECRAFT"].items():
            if alias in sc_config["ALIASES"]:
                return sc_key
        return None
