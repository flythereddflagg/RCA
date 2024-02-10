
import yaml

from .dict_obj import DictObj

def load_yaml(yaml_path):
        with open(yaml_path) as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.Loader)
        return DictObj(**yaml_data)