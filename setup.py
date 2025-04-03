import sys
from cx_Freeze import setup, Executable

# VERSION file contains the name of the version to be next released.
# INCREMENT VERSION AFTER EVERY RELEASE
with open("./VERSION") as f:
    VERSION = f.read().strip()

game_description = """Red Castle Avenger - The Game"""

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages'      : ['src'], 
    'excludes'      : ['cx_freeze'],
    'include_files' : [
        ("assets", "assets"),
        "VERSION",
        "README.md",
        "LICENSE"
    ]
}

base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('./main.py', base=base, target_name = 'RCA')
]

setup_options = {
    "name"           : 'RCA',
    "version"        : VERSION,
    "description"    : game_description,
    "options"        : {'build_exe': build_options},
    "executables"    : executables
}


setup(**setup_options)
# to build:
# conda install pyyaml pygame cx_freeze
# OR
# pip install pyyaml pygame cx_freeze
# python setup.py build
