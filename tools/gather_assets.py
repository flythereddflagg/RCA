
import os
import shutil
import pathlib

def gather_assets():
    text_matches = [".png", "/", ".yaml", ".json", ".ttf", ".mp3", ".ogg"]
    non_matches = ["http:", "#"]
    tmp_path = "./build/tmp_assets"
    src_path = "./assets"

    # Make the asset directory
    os.makedirs(tmp_path, exist_ok=True)
    asset_paths = []

    for filename in pathlib.Path(src_path).glob("**/*"):
        if not(str(filename).endswith(".json") or str(filename).endswith(".yaml")):
            continue
        asset_paths.append(filename)
        orphan_files = []
        prefix = ""
        with open(filename) as f:
            lines = f.readlines()
        for line in lines:
            if any([thing in line for thing in text_matches]):
                if any([thing in line for thing in non_matches]):
                    continue
                path = (
                    line.strip().split("\"")[-2].replace("\"", "")
                    if str(filename).endswith(".json") else
                    line.strip().split(": ")[-1].replace("\"", "")
                )
                if path.endswith("/"):
                    prefix = path
                elif "/" not in path:
                    orphan_files.append(pathlib.Path(path))
                else:                
                    asset_paths.append(pathlib.Path(path))

        for path in orphan_files:
            if not prefix:
                prefix = "/".join(str(filename).split("/")[:-1])
            new_file = pathlib.Path(prefix) / pathlib.Path(path)
            asset_paths.append(new_file)

    does_not_exist = []
    for path in asset_paths:
        if not path.exists():
            does_not_exist.append(path)
            continue

        new_path = pathlib.Path(tmp_path) / path
        os.makedirs(new_path.parents[0], exist_ok=True)
        shutil.copyfile(path, new_path)



