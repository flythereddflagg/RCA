CC = gcc
CFLAGS = -g -Wall #-fanalyzer
SRC = ./csrc/main.c
TEST_SRC = csrc_test/draw_texture_pro.c
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

get_raylib: clean_all
	mkdir -p ./lib
	git clone --depth 1 https://github.com/raysan5/raylib.git .raylib
	cd .raylib/src/ && $(MAKE) PLATFORM=PLATFORM_DESKTOP
	cd ../..
	cp .raylib/LICENSE ./lib
	cp .raylib/src/libraylib.a ./lib

# https://github.com/andrewmd5/cyaml.git .cyaml

preprocess:
	$(CC) $(CFLAGS) -E $(SRC) -o $(OUT).o $(INCLUDES)

obj:
	$(CC) $(CFLAGS) -c $(SRC) -o $(OUT).o $(INCLUDES)

build:
	$(CC) $(CFLAGS) $(SRC) -o $(OUT) $(LIBS) $(INCLUDES)

test:
	$(CC) $(CFLAGS) $(TEST_SRC) -o $(OUT) $(LIBS) $(INCLUDES)
	@echo "-- BUILD COMMAND COMPLETE --"
	./$(OUT)

run: build
	@echo "-- BUILD COMMAND COMPLETE --"
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
