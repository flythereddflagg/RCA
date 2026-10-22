CC = gcc
CFLAGS = -g -Wall #-fanalyzer
SRC ?= ./csrc/main.c
SRC_DIR = ./csrc
INCLUDE_DIR = ./include
RAYLIB_VERSION = 6.0
TMP_TXT = mem_check_all.txt
# TEST_SRC = csrc/bitmask.c
LIBS = -L./lib -lm -lyaml 
LIBS += -lraylib '-Wl,-rpath,$$ORIGIN/lib' # needed to point to .so files
# LIBS += -l:libraylib.so
# LIBS += -l:libraylib.so.6.0.0
# LIBS += -l:libraylib.so.600
# LIBS += -l:libraylib.a

ALL_DEPS = $(shell gcc $(SRC) -MM -I./include -I./csrc | sed -e 's/include\/[a-z]*\.h //g' -e 's/[a-z]*\.o:\s//g' -e 's/csrc\/[a-z]*\.c//g' -e 's/.h/.c/g' -e 's/ \\//g')



ALL_MAINS = $(shell find $(SRC_DIR)/*.c | sed -e 'y/abcdefghijklmnopqrstuvwxyz/ABCDEFGHIJKLMNOPQRSTUVWXYZ/' -e 's/.*CSRC\//__/g' -e 's/\.C/_MAIN__/g')

ALL_C = $(shell find $(SRC_DIR)/*.c)

# COMP_ALL = $(foreach (file, directive), ($(ALL_C), $(ALL_MAINS)), \
# 	echo "-- BUILDING $(file) --";\
# 	$(CC) $(CFLAGS) $(file) -o $(OUT) $(LIBS) $(INCLUDES)\
# 	-DTEST_ALL -D$(directive);\
# 	echo "-- BUILD COMMAND COMPLETE FOR $(file) --";\
# 	./$(OUT);\
# )

COMP_ALL = $(foreach (file, directive), ($(ALL_C), $(ALL_MAINS)), \
	echo  $$file with $$directive;\
)
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
INCLUDES = -I$(INCLUDE_DIR) -I$(SRC_DIR)
VALGRIND_OPTS ?=

.PHONY: all clean clean_all build run get_raylib help python flatpak appimage

all:help

help:
	@echo "Usage: make [build|run|clean|clean_all|get_raylib|help|python|flatpak|appimage]"

# get version 6.0 of raylib
# TODO get the right version of raylib by system detection.
get_raylib:
	mkdir -p ./lib
	wget https://github.com/raysan5/raylib/releases/download/$(RAYLIB_VERSION)/raylib-$(RAYLIB_VERSION)$(OS_VERSION)$(ZIP)
	$(UNZIP) ./raylib-$(RAYLIB_VERSION)$(OS_VERSION)$(ZIP)
	cp ./raylib-$(RAYLIB_VERSION)$(OS_VERSION)/lib/* ./lib
	mv ./raylib-$(RAYLIB_VERSION)$(OS_VERSION)/LICENSE ./lib/RAYLIB_LICENSE
	rm -rf ./raylib-$(RAYLIB_VERSION)$(OS_VERSION)
	rm -rf **.tar*
	rm -rf **.zip*

get_raylib_web:
	mkdir -p ./lib
	wget https://github.com/raysan5/raylib/releases/download/6.0/raylib-6.0_webassembly.zip
	unzip ./raylib-6.0_webassembly.zip
	cp ./raylib-6.0_webassembly/lib/* ./lib
	mv ./raylib-6.0_webassembly/LICENSE ./lib/RAYLIB_LICENSE
	rm -rf ./raylib-6.0_webassembly
	rm -rf **.tar*
	rm -rf **.zip*

get_deps: clean_all get_raylib

web:
	emcc -o game.html ./csrc/main.c -Os -Wall ./lib -I./csrc -I./include -L. -L./lib -s USE_GLFW=3 -DPLATFORM_WEB

format:
	clang-format -i $(SRC_DIR)/*.*
	clang-format -i $(INCLUDE_DIR)/*.*

preprocess:
	$(CC) $(CFLAGS) -E $(SRC) -o $(OUT).o $(INCLUDES)

obj:
	$(CC) $(CFLAGS) -c $(SRC) -o $(OUT).o $(INCLUDES)

debug:
	gdb ./$(OUT) -ex run -ex bt

build:
	$(CC) $(CFLAGS) $(SRC) -o $(OUT) $(LIBS) $(INCLUDES)
	@echo "-- BUILD COMMAND COMPLETE --"

test_all: $(ALL_C)
	$(COMP_ALL)

mem_all: $(ALL_MAINS_SRC)
	@echo "" > $(TMP_TXT)
	for file, directive in $^; do\
		echo "-- BUILDING $$file --";\
		$(CC) $(CFLAGS) $$file -o $(OUT) $(LIBS) $(INCLUDES) -DTEST_ALL;\
		echo "-- BUILD COMMAND COMPLETE FOR $$file --";\
		echo "-- BUILD COMMAND COMPLETE FOR $$file --" >> $(TMP_TXT);\
		valgrind ./$(OUT) 2>> $(TMP_TXT);\
	done
	./valgrind_summary.sh

test:
	$(CC) $(CFLAGS) $(ALL_DEPS) -o $(OUT) $(LIBS) $(INCLUDES) -DTEST -D$(MAIN_DIRECTIVE)
	@echo "-- BUILD COMMAND COMPLETE --"
	./$(OUT)

mem_check: test
	valgrind ./$(OUT) $(VALGRIND_OPTS)

run: build
	./$(OUT)

python:
	python setup.py build

flatpak:
	flatpak-builder --force-clean ./dist io.github.flythereddflagg.rca.yml
	flatpak build-import-bundle ./dist io.github.flythereddflagg.rca

appimage:
	mkdir -p ./dist/AppDir/usr/bin
	cp ./docs/RCA.desktop ./dist/AppDir/
	cp ./assets/block/game_icon_rev1.png ./dist/AppDir/
	cp -r ./build/exe.linux-x86_64-3.12/* ./dist/AppDir/
	cp ./docs/AppRun ./dist/AppDir/
	chmod +x ./dist/AppDir/AppRun
	ARCH=x86_64 ~/appimages/appimagetool-x86_64.AppImage ./dist/AppDir RCA.AppImage

clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./.flatpak-builder
	rm -f *.AppImage
	rm -f $(OUT)
	rm -f *.o
	rm -f $(TMP_TXT)

clean_all: clean
	rm -rf ./lib
	rm -rf ./.raylib
	rm -rf **.tar*
	rm -rf **.zip*

