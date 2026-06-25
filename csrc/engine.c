#ifndef __ENGINE_C__
#define __ENGINE_C__
#include "dbg.h"
#include "raylib.h"
#include <stdbool.h>

#include "node.c"
#include "tools.c"
#include "scene.c"

#define INIT_PATH "./assets/init.yaml" // this is NOT supposed to be here
#define MAX_INPUTS 6
#define SPEED 200
// TODO make an engine module
typedef enum { NO_DIR, UP, RIGHT, DOWN, LEFT } Direction;

typedef struct GameData *Game; 

struct GameData{
    Yaml settings;
    bool debug;
    bool running;
    bool paused;
    Scene scene;
    Scene *saved_scenes;
    RenderTexture2D draw_surface;
    void *input;

    
};

void input(Direction *inputs) {
    if (IsKeyDown(KEY_UP))
        inputs[0] = UP;
    if (IsKeyDown(KEY_DOWN))
        inputs[1] = DOWN;
    if (IsKeyDown(KEY_LEFT))
        inputs[2] = LEFT;
    if (IsKeyDown(KEY_RIGHT))
        inputs[3] = RIGHT;
}

void logic(Direction *inputs, NodeArray *nodes) {
    Node larry = nodes->arr[1];
    double dist = SPEED * GetFrameTime();
    for (int i = 0; i < MAX_INPUTS; i++) {
        switch (inputs[i]) {
        case UP:
            larry->decal->position.y -= dist;
            break;

        case DOWN:
            larry->decal->position.y += dist;
            break;

        case RIGHT:
            larry->decal->position.x += dist;
            break;

        case LEFT:
            larry->decal->position.x -= dist;
            break;

        default:
            break;
        }
        inputs[i] = 0;
    }
}

void draw_frame(NodeArray *nodes, RenderTexture2D v_screen) {
    BeginTextureMode(v_screen);
    ClearBackground(BLACK);
    for (int i = 0; i < nodes->len; i++)
        DrawTexture(nodes->arr[i]->decal->image,
                    nodes->arr[i]->decal->position.x,
                    nodes->arr[i]->decal->position.y, WHITE);
    EndTextureMode();
    double window_aspect_ratio = 1.0f * GetScreenWidth() / GetScreenHeight();
    double virtual_aspect_ratio =
        1.0f * v_screen.texture.width / v_screen.texture.height;
    float new_width = (window_aspect_ratio < virtual_aspect_ratio
                           ? GetScreenWidth()
                           : GetScreenHeight() * virtual_aspect_ratio);
    float new_height = (window_aspect_ratio < virtual_aspect_ratio
                            ? GetScreenWidth() / virtual_aspect_ratio
                            : GetScreenHeight());
    BeginDrawing();
    ClearBackground(BLACK);
    DrawTexturePro(v_screen.texture,
                   (Rectangle){0.0f, 0.0f, (float)v_screen.texture.width,
                               (float)-v_screen.texture.height},
                   (Rectangle){(GetScreenWidth() - new_width) / 2.0,
                               (GetScreenHeight() - new_height) / 2.0,
                               new_width, new_height},
                   (Vector2){0, 0},
                   0.0f, // rotation
                   WHITE);
    EndDrawing();
}

RenderTexture2D init_screen(Yaml settings) {
    int resolution = Yaml_get(settings, "RESOLUTION")._int_;
    int scale = Yaml_get(settings, "SCALE")._int_;
    char *title = Yaml_get(settings, "title")._str_;
    double aspect_ratio = (1.0f * Yaml_get(settings, "/ASPECT_RATIO[0]")._int_ /
                           Yaml_get(settings, "/ASPECT_RATIO[1]")._int_);

    SetConfigFlags(FLAG_WINDOW_RESIZABLE | FLAG_VSYNC_HINT);
    InitWindow((int)(resolution * aspect_ratio * scale), resolution * scale,
               title);
    SetTargetFPS(Yaml_get(settings, "FPS")._int_);
    SetExitKey(KEY_BACKSPACE);
    RenderTexture2D v_screen =
        LoadRenderTexture((int)(resolution * aspect_ratio), resolution);
    check(IsRenderTextureValid(v_screen), "render texture not loaded");
    // SetTextureFilter(v_screen.texture, TEXTURE_FILTER_BILINEAR); // todo
    // figure out what this does.

error:
    return v_screen;
}
Game Game_new(const char *init_path){
    return NULL;
}
void Game_delete(Game game){}

int Game_run(Game game) {
    // init
    Node mem[MAX_NODES];
    NodeArray nodes = (NodeArray){.len = 0, .arr = &(mem[0])};
    
    // Yaml settings = Yaml_load(init_path);
    Yaml settings = Yaml_load(INIT_PATH);
    check(settings, "Settings could not load");

    // void *scene = NULL;
    // void *saved_scenes = NULL;

    RenderTexture2D v_screen = init_screen(settings);
    check(IsRenderTextureValid(v_screen), "render texture not loaded");
    Image icon = LoadImage(Yaml_get(settings, "icon")._str_);
    SetWindowIcon(icon);

    Direction input_array[MAX_INPUTS] = {0};
    Direction *inputs = &(input_array[0]);

    NodeArray_add_node(
        &nodes, Node_new(Decal_new(
                    "./assets/scene/red_castle_valley/red_castle_valley_bg.png",
                    (Vector2){0, 0})));
    NodeArray_add_node(&nodes,
                       Node_new(Decal_new("./assets/actor/larry/larry_base.png",
                                          (Vector2){300, 300})));

    // mainloop
    bool running = true;
    while (running) {
        if (WindowShouldClose())
            running = false;
        input(inputs);
        logic(inputs, &nodes);
        draw_frame(&nodes, v_screen);
    }
    // cleanup
    for (int i = 0; i < nodes.len; i++)
        nodes.arr[i]->delete (nodes.arr[i]);
    UnloadRenderTexture(v_screen);
    Yaml_delete(settings);
    CloseWindow();
    UnloadImage(icon);
    return 0;

error:
    // cleanup
    for (int i = 0; i < nodes.len; i++)
        nodes.arr[i]->delete (nodes.arr[i]);
    UnloadRenderTexture(v_screen);
    Yaml_delete(settings);
    CloseWindow();
    UnloadImage(icon);
    return 1;
}
#endif