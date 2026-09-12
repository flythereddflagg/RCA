#ifndef __ENGINE_C__
#define __ENGINE_C__
#ifndef __MAIN__
#define __MAIN__
#define __ENGINE_MAIN__
#endif

#include "core.h"
#include "raylib.h"
#include <stdbool.h>

#include "input.c"
#include "node.c"
#include "scene.c"

#include "dict.c"
#include "valarray.c"
#include "yaml_parse.c"

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

RenderTexture2D Game_init_screen(Dict settings) {
    SetTraceLogLevel(LOG_WARNING);
    RenderTexture2D v_screen;
    int resolution = Dict_get(settings, "RESOLUTION", EMPTYVAL)._int_;
    int scale = Dict_get(settings, "SCALE", EMPTYVAL)._int_;
    char *title = Dict_get(settings, "title", EMPTYVAL)._str_.cstring;
    ValArray aspect_ratio_parts =
        Dict_get(settings, "ASPECT_RATIO", EMPTYVAL)._arr_;
    check(aspect_ratio_parts, "ValArray Failed to load.");
    double aspect_ratio = (1.0f * ValArray_get_at(aspect_ratio_parts, 0)._int_ /
                           ValArray_get_at(aspect_ratio_parts, 1)._int_);

    SetConfigFlags(FLAG_WINDOW_RESIZABLE | FLAG_VSYNC_HINT);
    InitWindow((int)(resolution * aspect_ratio * scale), resolution * scale,
               title);
    SetTargetFPS(Dict_get(settings, "FPS", EMPTYVAL)._int_);
    SetExitKey(KEY_BACKSPACE);
    v_screen = LoadRenderTexture((int)(resolution * aspect_ratio), resolution);
    check(IsRenderTextureValid(v_screen), "render texture not loaded");
    // TODO figure out what this does.
    // SetTextureFilter(v_screen.texture, TEXTURE_FILTER_BILINEAR);

error:
    return v_screen;
}

void Game_draw_frame(Game self) {
    RenderTexture2D v_screen = self->draw_surface;
    double window_aspect_ratio = 1.0f * GetScreenWidth() / GetScreenHeight();
    double virtual_aspect_ratio =
        1.0f * v_screen.texture.width / v_screen.texture.height;
    float new_width = (window_aspect_ratio < virtual_aspect_ratio
                           ? GetScreenWidth()
                           : GetScreenHeight() * virtual_aspect_ratio);
    float new_height = (window_aspect_ratio < virtual_aspect_ratio
                            ? GetScreenWidth() / virtual_aspect_ratio
                            : GetScreenHeight());
    // draw everyting to the virtual screen
    BeginTextureMode(v_screen);
    ClearBackground(BLACK);
    // for (int i = 0; i < nodes->len; i++)
    //     DrawTexture(nodes->arr[i]->decal->image,
    //                 nodes->arr[i]->decal->position.x,
    //                 nodes->arr[i]->decal->position.y, WHITE);
    EndTextureMode();

    // then scale virtual screen to fit and then draw to the actual screen
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

Game Game_new(const char *init_path) {
    Game game = (Game)malloc(sizeof(struct GameData));
    check_mem(game);
    game->settings = YamlParse_process_yaml_file(init_path)._dict_;
    check(game->settings, "Settings could not load");
    game->debug = false;
    game->running = false;
    game->paused = false;
    game->input = Input_new(game);
    game->draw_surface = Game_init_screen(game->settings);

    game->icon =
        LoadImage(Dict_get(game->settings, "icon", EMPTYVAL)._str_.cstring);
    game->scene = NULL;
    game->saved_scenes = NULL;
    SetWindowIcon(game->icon);
error:
    return game;
}
Game Game_delete(Game game) {
    if (game) {
        UnloadImage(game->icon);
        UnloadRenderTexture(game->draw_surface);
        game->input = Input_delete(game->input);
        game->settings = Dict_delete(game->settings);
        CloseWindow();
        free(game);
    }

    return NULL;
}
Scene Game_load_scene(Game game, char *yaml_path, ValArray add_in) {
    return NULL;
}

int Game_logic(Game game) { return 0; }

int Game_loop_steps(Game game) {
    Input_update(game->input);
    // check(Game_logic(game), "Logic Error with exit code %d");
    Game_draw_frame(game);
}

int Game_run(Game game) {
    Game_load_scene(
        game, Dict_get(game->settings, "inital_scene", EMPTYVAL)._str_.cstring,
        Dict_get(game->settings, "init_add_in", EMPTYVAL)._arr_);

#if defined(PLATFORM_WEB)
    emscripten_set_main_loop_arg(
        UpdateDrawFrame, game, Dict_get(game->settings, "FPS", EMPTYVAL)._int_,
        true);
#else
    // mainloop
    game->running = true;
    while (game->running) {
        if (WindowShouldClose())
            game->running = false;
        Game_loop_steps(game);
    }
#endif

    return 0;

    // error:
    //     return 1;
}

#ifdef __ENGINE_MAIN__
int main() { return 0; }
#endif
#endif
