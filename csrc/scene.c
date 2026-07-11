#ifndef __SCENE_C__
#define __SCENE_C__
#include "node.c"
#include "yaml.c"
#include <stdbool.h>

// TODO implement Scene logic

typedef struct SceneData *Scene;
struct SceneData {
    void *game;
    bool paused;
    bool occupied;
    char *id;
    char **draw_layers;
    char **group_names;
    NodeArray *groups;
    NodeArray all_nodes;
    NodeArray active_nodes;
    Node bg_ref;
    Yaml init;
};
void Scene_new(void);
void Scene_delete(void);
void Scene_update(void);
void Scene_place_node(void);
void Scene_refresh(void);
void Scene_serialize(void);
void Scene_node_by_id(void);
void Scene_node_ids(void);
void Scene_node_in_groups(void);

#endif
