import os


CC = "gcc"
# CFLAGS = "-g -Wall -fanalyzer"
CFLAGS = "-g -Wall"
SRC = "./csrc/**/*.c ./csrc/*.c"
SRC_DIR = "./csrc"
INCLUDE_DIR = "./include"
RAYLIB_VERSION = "6.0"
TMP_TXT = "mem_check_all.txt"

LIBS = "-L./lib -lm -lyaml" 
LIBS += "-lraylib '-Wl,-rpath,$$ORIGIN/lib'" # needed to point to .so files
"""
CORE_TESTS = $(shell grep "__.*_MAIN__" ./tests/test_core.c | sed -e "s/#ifdef //g")
"""

if (os.name == )
ifeq ($(OS),Windows_NT)
	LIBS += -lgdi32 -lwinmm -Wl,--defsym,stat64i32=_stat64
	OUT = main.exe
	ZIP = .zip
	UNZIP = unzip
	OS_VERSION = _win64_mingw-w64
	
else
	LIBS += -lX11
	OUT = main
	ZIP = .tar.gz
	UNZIP = tar -xvf
	ifneq ($(filter arm%,$(UNAME_P)),)
		OS_VERSION = _linux_arm64
	else
    	OS_VERSION = _linux_amd64
	endif
	
endif