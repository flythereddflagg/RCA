#ifndef __ENGINE_H__
#define __ENGINE_H__
typedef struct GameData *Game;
#include "dict.h"
#include "raylib.h"

#include "dbg.h"
#include "raylib.h"
#include <stdbool.h>

#include "input.h"
#include "node.h"
#include "scene.h"

#include "dict.h"
#include "valarray.h"
#include "yaml_parse.h"
#include <stdlib.h>

#define MAX_INPUTS 6
#define SPEED 200

struct GameData {
    Dict settings;
    bool debug;
    bool running;
    bool paused;
    Input input;
    RenderTexture2D draw_surface;
    Image icon;
    Scene scene;
    Scene *saved_scenes;
};

RenderTexture2D Game_init_screen(Dict settings);
int Game_draw_frame(Game game);
Game Game_new(const char *init_path);
Game Game_delete(Game game);
int Game_load_scene(Game game, char *yaml_path, ValArray add_in);
int Game_logic(Game game);
int Game_loop_steps(Game game);
int Game_run(Game game);

#endif
