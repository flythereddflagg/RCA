import sys
from cx_Freeze import setup, Executable

game_description = """Red Castle Avenger - The Game"""

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages'      : ['src'], 
    'excludes'      : ['cx_freeze'],
    'include_files' : [
        ("assets", "assets")
    ]
}

base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('./main.py', base=base, target_name = 'RCA')
]

setup_options = {
    "name"           : 'RCA',
    "version"        : '0.1.3',
    "description"    : game_description,
    "options"        : {'build_exe': build_options},
    "executables"    : executables
}


setup(**setup_options)
# to build:
# conda init powershell
# conda activate pygame_compile 
# python setup.py build
