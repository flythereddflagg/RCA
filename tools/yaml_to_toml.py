import pathlib
import yaml
import sys



for file in pathlib.Path(".").glob("./**/*.yaml"):
    subs = []
    
    with open(file) as f:
        content = yaml.load(f.read(), Loader=yaml.Loader)
    with open(str(file)[:-5]+".toml", 'w') as f:
        print("# converted from:", file, file=f)
        for key, item in content.items():
            if isinstance(item, dict):
                subs.append([key, item])
            else:
                if isinstance(item, str):
                    item = f"\"{item}\""
                elif isinstance(item, bool):
                    item = str(item).lower()
                elif isinstance(item, list):
                    item = str(item).replace(':', ' =')
                elif item is None:
                    item = "\"\""
                print(f"{key} = {item}", file=f)
        for key, item in subs:
            print(f"\n[{key}]", file=f)
            for subkey, subitem in item.items():
                if isinstance(subitem, str):
                    subitem = f"\"{subitem}\""
                # print(f"{key}.{subkey} = {subitem}")
                print(f"{subkey} = {subitem}", file=f)
            print("", file=f)

