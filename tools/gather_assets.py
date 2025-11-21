
import os
import shutil
import pathlib

import re
import json
import yaml

# Make the asset directory
os.makedirs("./build/tmp_assets", exist_ok=True)

for filename in pathlib.Path(".").glob("**/*.json"):
    print(filename)
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if any([thing in line for thing in [".png", "/", ".yaml", ".json"]]):
            print("\t", line.strip().split("\"")[-2]) 


    

for filename in pathlib.Path(".").glob("**/*.yaml"):
    print(filename)
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if any([thing in line for thing in [".png", "/", ".yaml", ".json"]]):
            print("\t", line.strip().split("\"")[-2]) 

