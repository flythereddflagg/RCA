import pathlib
import yaml
import sys


def map_to_toml(key, item):
    if isinstance(item, str):
        return f"{key} = \"{item}\""
    elif isinstance(item, bool):
        return f"{key} = {str(item).lower()}"
    elif isinstance(item, list):
        return list_str_repr(item, key)
    elif item is None:
        return f"{key} = \"\""
    else:
        return f"{key} = {item}"    
    

def list_str_repr(a_list:list, master_key:str):
    out_str = ""
    if a_list and isinstance(a_list[0], dict):
        for item in a_list:
            out_str += f"\n[[{master_key}]]\n"
            for key, val in item.items():
                out_str += f"{key} = {map_to_toml(key, val)}\n"
    else: return f"{master_key} = {str(a_list)}"
    
    return out_str

for file in pathlib.Path(".").glob("./**/*.yaml"):
    subs = []
    
    with open(file) as f:
        content = yaml.load(f.read(), Loader=yaml.Loader)
    with open(str(file)[:-5]+".toml", 'w') as f:
    # if True:
    #     f = sys.stdout
        print("#--------\n# converted from:", file, file=f)
        for key, item in content.items():
            if isinstance(item, dict):
                subs.append([key, item])
            else:
                print(map_to_toml(key, item), file=f)
        for key, item in subs:
            print(f"\n[{key}]", file=f)
            for subkey, subitem in item.items():
                sub_key_val = map_to_toml(subkey, subitem)
                print(sub_key_val, file=f)
            print("", file=f)

