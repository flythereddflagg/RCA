import sys
sys.path.append("..")

from RCA.src.tools import load_yaml

save_file = "/home/redd/.local/share/rca/saves/save_file.yaml"
src_file = "./assets/scene/mansion_yard.yaml"

sav_data = load_yaml(save_file)["scenes"][src_file]
src_data = load_yaml(src_file)
# print(sav_data, src_data)
print(set(sav_data) ^ set(src_data))