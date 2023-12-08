from app.core.login import load_token_env
import json
import importlib


def load_plugins():
    with open('app/plugins.json', 'r') as f:
        return json.load(f)


def import_module(name, path):
    return importlib.import_module(name, path)


def load_all_plugins():
    plugins_list = load_plugins()

    plugins = {}
    for plugin in plugins_list['plugins']:
        plugins[plugin['name']] = import_module(f"app.plugins.{plugin['path']}", ".")
        plugins[plugin['name']].load_success()

    return plugins


class Sonar:
    def __init__(self):
        self.plugins = load_all_plugins()
        load_token_env()
