import sys
sys.path.append(".")

import pathlib
from src.tools import load_yaml, save_yaml

path = pathlib.Path(".")

for filename in path.glob("./assets/scene/*.yaml"):
    print(filename)
    yaml = load_yaml(filename)
    if "nodes" in yaml: continue
    node_list = []
    for key, obj in yaml.items():
        if not isinstance(obj, list) or key == "layers": continue
        for node in obj:
            if "groups" not in node:
                node["groups"] = []
            node["groups"].append(key)
        node_list.extend(obj)

    output_yaml = {"layers":yaml["layers"], "nodes": node_list}    
    # print(output_yaml)
    save_yaml(output_yaml, filename)
    # break