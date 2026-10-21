#ifndef __ENGINE_H__
#define __ENGINE_H__
#include "scene.h"
typedef struct GameData *Game;
RenderTexture2D Game_init_screen(Dict settings);
void Game_draw_frame(Game self);
Game Game_new(const char *init_path);
Game Game_delete(Game game);
Scene Game_load_scene(Game game, char *yaml_path, ValArray add_in);
int Game_logic(Game game);
int Game_loop_steps(Game game);
int Game_run(Game game);

#endif
