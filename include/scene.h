#ifndef __SCENE_H__
#define __SCENE_H__
typedef struct SceneData *Scene;
#include "dbg.h"
#include "dict.h"
#include "engine.h"
#include "lstring.h"
#include "node.h"
#include "yaml_parse.h"
#include <stdbool.h>
#define BG_REF "bg_ref"

// TODO implement Scene logic
Scene Scene_delete(Scene);
int Scene_place_node(Scene scene, Node node, ValArray groups, ValArray start,
                     bool active);

void Scene_refresh(void);
void Scene_serialize(void);
void Scene_node_ids(void);
void Scene_node_in_groups(void);

Scene Scene_new(Game game, char *yaml_path, Dict yaml_data, ValArray add_in);
Scene Scene_delete(Scene scene);
int Scene_update(Scene scene);
int Scene_setup(Scene scene);
int Scene_deconstruct(Scene scene);
Node Scene_node_by_id(Scene scene, char *node_id);

#endif
