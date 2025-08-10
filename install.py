import venv
import subprocess
import sys

# TODO: setup an autobuild system
virtual_environment = venv.create("./install", clear=True)

activate = (
    "./install/Scripts/activate.bat"
    if sys.platform=='win32' else 
    "source ./install/bin/activate"
)
subprocess.run(activate, shell=True, check=True)
install_commands = [
    "activate"
    "python -m pip install -r ./requirements.txt",
    "python setup.py build",
    "deactivate"
]
for command in install_commands:
    subprocess.call(command, check=True)

print("install completed without errors!")




