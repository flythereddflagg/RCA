import pathlib
import yaml
import tomllib
import sys


def map_to_toml(key, item, master_key=None):
    if isinstance(item, str):
        return f"{key} = \"{item}\""
    elif isinstance(item, bool):
        return f"{key} = {str(item).lower()}"
    elif isinstance(item, list):
        return list_str_repr(item, key)
    elif isinstance(item, dict):
        if master_key:
            key = f"{master_key}.{key}"
        return dict_str_repr(item, key)
    elif item is None:
        return f"{key} = \"\""
    else:
        return f"{key} = {item}"    
    
def dict_str_repr(a_dict:dict, master_key:str):
    out_str = f"[{master_key}]\n"
    for key, item in a_dict.items():
        out_str += f"{map_to_toml(key, item, master_key=master_key)}\n"
    
    return out_str

def list_str_repr(a_list:list, master_key:str):
    out_str = ""
    if a_list and isinstance(a_list[0], dict):
        for item in a_list:
            out_str += f"\n[[{master_key}]]\n"
            for key, val in item.items():
                out_str += f"{map_to_toml(key, val, master_key=master_key)}\n"
    else: return f"{master_key} = {str(a_list)}"
    
    return out_str

def validate_files(file1, file2):
    contents = [None, None]
    for i, file_ in enumerate((file1, file2)):
        # breakpoint()
        if file_.endswith(".yaml"):
            with open(file_) as f:
                d1 = yaml.load(f.read(), Loader=yaml.Loader)
        elif file_.endswith(".toml"):
            with open(file_, 'rb') as f:
                d1 = tomllib.load(f)
        contents[i] = d1
    
    
    one, two = contents
    assert one == two, f"{(file1,file2)}\n{one}\n\n|||\n\n{two}"
    

def main():
    for file in pathlib.Path(".").glob("./**/*.yaml"):
        subs = []
        
        with open(file) as f:
            content = yaml.load(f.read(), Loader=yaml.Loader)
        with open(str(file)[:-5]+".toml", 'w') as f:
        # if not "animations" in content.keys(): continue
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
                    sub_key_val = map_to_toml(subkey, subitem, master_key=key)
                    print(sub_key_val, file=f)
                print("", file=f)
        # break
        validate_files(str(file)[:-5]+".toml", str(file)[:-5]+".yaml")

if __name__ == "__main__":
    main()