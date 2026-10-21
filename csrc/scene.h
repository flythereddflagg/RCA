#ifndef __SCENE_H__
#define __SCENE_H__
typedef struct SceneData *Scene;
#include "engine.h"
#include "node.h"


Scene Scene_new(Game game, char *yaml_path, Dict yaml_data, ValArray add_in);
Scene Scene_delete(Scene scene);
int Scene_update(Scene scene);
int Scene_setup(Scene scene);
int Scene_deconstruct(Scene scene);
Node Scene_node_by_id(Scene scene, char *node_id);

#endif
