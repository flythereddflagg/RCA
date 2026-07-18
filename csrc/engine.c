#ifndef __ENGINE_C__
#define __ENGINE_C__
#include "dbg.h"
#include "raylib.h"
#include <stdbool.h>

#include "node.c"
#include "scene.c"
#include "yaml.c"
#include "input.c"

#define MAX_INPUTS 6
#define SPEED 200

typedef struct GameData *Game;

struct GameData {
    Yaml settings;
    bool debug;
    bool running;
    bool paused;
    Input input;
    RenderTexture2D draw_surface;
    Image icon;
    Scene scene;
    Scene *saved_scenes;
};

RenderTexture2D Game_init_screen(Yaml settings) {
    SetTraceLogLevel(LOG_WARNING); 
    int resolution = Yaml_get(settings, "RESOLUTION")._int_;
    int scale = Yaml_get(settings, "SCALE")._int_;
    char *title = Yaml_get(settings, "title")._str_;
    double aspect_ratio = (1.0f * Yaml_get(settings, "/ASPECT_RATIO[0]")._int_ /
                           Yaml_get(settings, "/ASPECT_RATIO[1]")._int_);

    SetConfigFlags(FLAG_WINDOW_RESIZABLE | FLAG_VSYNC_HINT);
    InitWindow((int)(resolution * aspect_ratio * scale), resolution * scale,
               title);
    SetTargetFPS(Yaml_get(settings, "FPS")._int_);
    log_info("FPS %d", Yaml_get(settings, "FPS")._int_);
    SetExitKey(KEY_BACKSPACE);
    RenderTexture2D v_screen =
        LoadRenderTexture((int)(resolution * aspect_ratio), resolution);
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
    Game game = (Game) malloc(sizeof(struct GameData));
    check_mem(game);
    game->settings = Yaml_load(init_path);
    check(game->settings, "Settings could not load");
    game->debug = false;
    game->running = false;
    game->paused = false;
    game->input = Input_new(game);
    game->draw_surface = Game_init_screen(game->settings);
    log_info("icon %s", Yaml_get(game->settings, "icon")._str_);

    game->icon = LoadImage(Yaml_get(game->settings, "icon")._str_);
    game->scene = NULL;
    game->saved_scenes = NULL;
    SetWindowIcon(game->icon);
error:
    return game; 
}
Game Game_delete(Game game) {
    UnloadImage(game->icon);
    UnloadRenderTexture(game->draw_surface);
    game->input = Input_delete(game->input);
    game->settings = Yaml_delete(game->settings);
    CloseWindow();
    
    if (game)
        free(game);

    return NULL;
}

void Game_logic(Game game){;}

int Game_run(Game game) {
    // mainloop
    game->running = true;
    while (game->running) {
        if (WindowShouldClose())
            game->running = false;
        Input_update(game->input);
        Game_logic(game);
        Game_draw_frame(game);
    }
    return 0;

error:
    return 1;
}
#endif
