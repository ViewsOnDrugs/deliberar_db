
import yaml
import os

dirname = os.path.dirname(__file__)


def load_lan(lang):
    # load organization library
    json_file = os.path.join(dirname, f'{lang}.yaml')
    with open(json_file, "r") as orgl:
        lang_dict = yaml.safe_load(orgl)
    return lang_dict

