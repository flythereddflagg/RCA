import sys
sys.path.append("..")

from RCA.src.tools import load_yaml, save_yaml

def comp_obj(obj1, obj2):
    if type(obj1) != type(obj2):
        print("type", type(obj1), type(obj2))
        return False
    elif (isinstance(obj1, list) and len(obj1) != len(obj2)):
        print("len", len(obj1), len(obj2))
        return False
    elif (isinstance(obj1, list)
        and not all([
            comp_obj(o1, o2) 
            for o1, o2 in zip(list(obj1), list(obj2))
        ])
    ):
        print("list")
        return False
    elif (isinstance(obj1, dict) and (set(obj1) ^ set(obj2))):
        print("keys", set(obj1) ^ set(obj2))
        return False
    elif (isinstance(obj1, dict)
        and not all([
            comp_obj(o1, o2) 
            for o1, o2 in zip(list(obj1.values()), list(obj2.values()))
        ])
    ):
        print("dict")
        return False
    elif (
        not isinstance(obj1, dict) 
        and not isinstance(obj1, list) 
        and obj1 != obj2
    ):
        print("obj", obj1, obj2)
        return False

    return True

save_file = "/home/redd/.local/share/rca/saves/save_file.yaml"
src_file = "./assets/scene/mansion_yard.yaml"

sav_data = load_yaml(save_file)["scenes"][src_file]
src_data = dict(load_yaml(src_file))
# print(sav_data, src_data)
print(comp_obj(sav_data, src_data))
(save_yaml(sav_data, "./diff1.yaml"), save_yaml(src_data, "./diff2.yaml"))
