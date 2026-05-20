
import os
import shutil
import pathlib
import re
import json

def gather_assets():
    text_matches = [".png", "/", ".yaml", ".json", ".ttf", ".mp3", ".ogg"]
    non_matches = ["http", "#"]
    tmp_path = "./build/tmp_assets"
    src_path = "./assets"
    file_types = [".png", ".yaml", ".json", ".ttf", ".mp3", ".ogg", ".txt"]

    # Make the asset directory
    os.makedirs(tmp_path, exist_ok=True)
    asset_paths = []


    for filename in pathlib.Path(src_path).glob("**/*"):
        if not any([
            str(filename).endswith(ending) 
            for ending in file_types
        ]):
            print("Skipping", filename)
            continue

        new_path = pathlib.Path(tmp_path) / filename
        os.makedirs(new_path.parents[0], exist_ok=True)
        print(f"Copying <{filename}> into assets")
        shutil.copyfile(filename, new_path)



if __name__ == "__main__":
    gather_assets()