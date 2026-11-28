import os as _os
import sys as _sys
import subprocess as _sp
import re as _re
import pathlib as _pl

CC = "gcc"
# CFLAGS = "-g -Wall -fanalyzer"
CFLAGS = "-g -Wall"
SRC = "./csrc/**/*.c ./csrc/*.c"
SRC_DIR = "./csrc"
INCLUDE_DIR = "./include"
INCLUDES = f"-I{INCLUDE_DIR}"
RAYLIB_VERSION = "6.0"
TMP_TXT = "mem_check_all.txt"
TEST_FILE = "./tests/test_core.c"
LIBS = " -L./lib -lm -lyaml" 
LIBS += " -lraylib '-Wl,-rpath,$ORIGIN/lib'" # needed to point to .so files

if _os.uname().sysname == 'Linux':
    LIBS += " -lX11"
    OUT = "main"
    ZIP = ".tar.gz"
    UNZIP = "tar -xvf"
    if _os.uname().machine == "x86_64":
        OS_VERSION = "_linux_amd64"
    else:
        OS_VERSION = "_linux_arm64"

elif os.uname().sysname == 'Windows':
    LIBS += " -lgdi32 -lwinmm -Wl,--defsym,stat64i32=_stat64"
    OUT = "main.exe"
    ZIP = ".zip"
    UNZIP = "unzip"
    OS_VERSION = "_win64_mingw-w64"

def RUN_CMD(cmd):
    print(cmd)
    res:'_sp.CompletedProcess' = _sp.run(cmd, shell=True)
    if res.returncode:
        print(f"Returned non-zero exit status {res.returncode}")
        _sys.exit()


def build():
    RUN_CMD(f"{CC} {CFLAGS} {SRC} -o {OUT} {LIBS} {INCLUDES}")
    print("-- BUILD COMMAND COMPLETE --")

def clean(): pass
def clean_all(): pass
def core():
    for filename in _pl.Path(".").glob(f"{SRC_DIR}/core/*.c"):
        print(filename)
        RUN_CMD(
            f"{CC} {CFLAGS} -c {filename} -o "\
            f"{str(filename)[:-2]}.o {INCLUDES}"
        )
        RUN_CMD(f"ar rcs ./lib/librca_core.a {SRC_DIR}/core/*.o")

def debug(): pass

def format():
    RUN_CMD(f"clang-format -i {SRC_DIR}/**/*.*")
    RUN_CMD(f"clang-format -i {SRC_DIR}/*.*")
    RUN_CMD(f"clang-format -i {INCLUDE_DIR}/*.*")

def get_raylib(): pass
def get_raylib_web(): pass
def get_deps(): pass

def help():
    command_txt = [
        thing 
        for thing in list(globals().keys()) 
        if thing == thing.lower() and "_" not in thing
    ]
    print(f"No command selected. Must be one of:\n{command_txt}")

def mem_all(): pass
def mem_check(): pass

def run():
    build()
    RUN_CMD(f"./{OUT}")

def test(tests:list):
    for main in tests:
        main = main.upper()
        RUN_CMD(
            f"{CC} {CFLAGS} {TEST_FILE} -o {OUT} {LIBS} {INCLUDES} "\
            f"-D__{main}_MAIN__ -lrca_core"
        )
        RUN_CMD(f"./{OUT}")

def test_all():
    with open("./tests/test_core.c") as f:
        mains = [line for line in f.readlines() if "MAIN" in line]
    print(mains)

def web(): pass


if __name__ == "__main__":
    command_txt = [
        thing 
        for thing in list(globals().keys()) 
        if thing == thing.lower() and not thing.startswith("_")
    ]
    if len(_sys.argv) < 2:
        help()
    else:
        if _sys.argv[1] not in command_txt:
            raise ValueError(f"invalid command supplied: '{_sys.argv[1]}'")
        recipe = globals()[_sys.argv[1]]
        if len(_sys.argv) > 2:
            recipe(_sys.argv[2:])
        else:
            recipe()
