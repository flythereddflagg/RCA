CC = gcc
CFLAGS = -g -Wall #-fanalyzer
SRC ?= ./csrc/main.c
SRC_DIR = ./csrc
RAYLIB_VERSION = 6.0
# TEST_SRC = csrc/bitmask.c
LIBS = -lraylib -L./lib -lm -lyaml 
LIBS += '-Wl,-rpath,$$ORIGIN/lib' # needed to point to .so files
ifeq ($(OS),Windows_NT)
	LIBS += -lgdi32 -lwinmm -Wl,--defsym,stat64i32=_stat64
	OUT = main.exe
	ZIP = .zip
	OS_VERSION = _win64_mingw-w64
	
else
	LIBS += -lX11
	OUT = main
	ZIP = .tar.gz
	ifneq ($(filter arm%,$(UNAME_P)),)
		OS_VERSION = _linux_arm64
	else
    	OS_VERSION = _linux_amd64
	endif
	
endif
INCLUDES = -I./include -I./csrc
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
	tar -xvf ./raylib-$(RAYLIB_VERSION)$(OS_VERSION)$(ZIP)
	cp ./raylib-$(RAYLIB_VERSION)$(OS_VERSION)/lib/* ./lib
	mv ./raylib-$(RAYLIB_VERSION)$(OS_VERSION)/LICENSE ./lib/RAYLIB_LICENSE
	rm -rf ./raylib-$(RAYLIB_VERSION)$(OS_VERSION)$(ZIP)
	rm -rf **.tar*
	rm -rf **.zip*


get_deps: clean_all get_raylib


preprocess:
	$(CC) $(CFLAGS) -E $(SRC) -o $(OUT).o $(INCLUDES)

obj:
	$(CC) $(CFLAGS) -c $(SRC) -o $(OUT).o $(INCLUDES)

build:
	$(CC) $(CFLAGS) $(SRC) -o $(OUT) $(LIBS) $(INCLUDES)
	@echo "-- BUILD COMMAND COMPLETE --"

test_all: $(SRC_DIR)/*.c
	for file in $^; do\
		echo "-- BUILDING $$file --";\
		$(CC) $(CFLAGS) $$file -o $(OUT) $(LIBS) $(INCLUDES) -DTEST_ALL;\
		echo "-- BUILD COMMAND COMPLETE FOR $$file --";\
		./$(OUT);\
	done


test:
	$(CC) $(CFLAGS) $(SRC) -o $(OUT) $(LIBS) $(INCLUDES) -DTEST
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

clean_all: clean
	rm -rf ./lib
	rm -rf ./.raylib
	rm -rf **.tar*
