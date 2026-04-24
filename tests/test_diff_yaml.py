import sys
sys.path.append("..")

from RCA.src.tools import load_yaml

def comp_obj(obj1, obj2):
    if (
        type(obj1) != type(obj2)
        or (
            isinstance(obj1, list) 
            and len(obj1) != len(obj2)
            and not all([
                comp_obj(o1, o2) 
                for o1, o2 in zip(list(obj1), list(obj2))
            ])
        )
        or (
            isinstance(obj1, dict)
            and (set(obj1) ^ set(obj2))
            and not all([
                comp_obj(o1, o2) 
                for o1, o2 in zip(list(obj1.values()), list(obj2.values()))
            ])
        )
        or(
            not isinstance(obj1, dict) 
            and not isinstance(obj1, list) 
            and obj1 != obj2
        )
        
    ):
        print(obj1, obj2)
        return False

    return True

save_file = "/home/redd/.local/share/rca/saves/save_file.yaml"
src_file = "./assets/scene/mansion_yard.yaml"

sav_data = load_yaml(save_file)["scenes"][src_file]
src_data = load_yaml(src_file)
# print(sav_data, src_data)
print(comp_obj(sav_data, src_data))