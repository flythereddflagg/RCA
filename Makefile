CC = gcc
CFLAGS = -g -Wall #-fanalyzer
SRC = ./csrc/main.c
TEST_SRC = csrc/bitmask.c
LIBS = -lraylib -L./lib -lm -lcyaml 
LIBS += '-Wl,-rpath,$$ORIGIN/lib' # needed to point to .so files
ifeq ($(OS),Windows_NT)
	LIBS += -lgdi32 -lwinmm
	OUT = main.exe
else
	LIBS += -lX11
	OUT = main
endif
INCLUDES = -I./include -I./csrc

.PHONY: all clean clean_all build run get_raylib help python flatpak appimage

all:help

help:
	@echo "Usage: make [build|run|clean|clean_all|get_raylib|help|python|flatpak|appimage]"

# get version 6.0 of raylib
get_raylib:
	mkdir -p ./lib
	wget https://github.com/raysan5/raylib/releases/download/6.0/raylib-6.0_linux_amd64.tar.gz
	tar -xvf ./raylib-6.0_linux_amd64.tar.gz
	cp ./raylib-6.0_linux_amd64/lib/* ./lib
	mv ./raylib-6.0_linux_amd64/LICENSE ./lib/RAYLIB_LICENSE
	rm -rf ./raylib-6.0_linux_amd64
	rm -rf **.tar*

get_cyaml:
	dir -p ./lib
	wget https://github.com/andrewmd5/cyaml/releases/download/v0.1.3/cyaml-linux-x64.tar.gz
	tar -xvf ./cyaml-linux-x64.tar.gz
	rm -rf **.tar*

get_deps: clean_all get_raylib get_cyaml


preprocess:
	$(CC) $(CFLAGS) -E $(SRC) -o $(OUT).o $(INCLUDES)

obj:
	$(CC) $(CFLAGS) -c $(SRC) -o $(OUT).o $(INCLUDES)

build:
	$(CC) $(CFLAGS) $(SRC) -o $(OUT) $(LIBS) $(INCLUDES)
	@echo "-- BUILD COMMAND COMPLETE --"

test:
	$(CC) $(CFLAGS) $(TEST_SRC) -o $(OUT) $(LIBS) $(INCLUDES) -DTEST_MAIN
	@echo "-- BUILD COMMAND COMPLETE --"
	./$(OUT)

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
