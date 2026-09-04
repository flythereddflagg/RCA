#ifndef __SCENE_C__
#define __SCENE_C__
#ifndef __MAIN__
#define __MAIN__
#define __SCENE_MAIN__
#endif
#include "core.h"
#include "dictarr.c"
#include "engine.c"
#include "lstring.c"
#include "node.c"
#include <stdbool.h>

// TODO implement Scene logic
Scene Scene_delete(Scene);

struct SceneData {
    Game game;
    bool paused;
    bool occupied;
    Lstring id;
    ValArray draw_layers;
    ValArray group_names;
    NodeArray *groups;
    NodeArray all_nodes;
    NodeArray active_nodes;
    Node bg_ref;
    Dict init;
};
Scene Scene_new(Game game, Lstring yaml_path, Dict yaml_data, ValArray add_in) {
    Scene self = (Scene)malloc(sizeof(struct SceneData));
    check_mem(self);
    self->game = game;
    self->paused = false;
    self->id = yaml_path;
    self->init = yaml_data
                     ? yaml_data
                     : YamlParse_process_yaml_file(yaml_path.cstring)._dict_;
    ValArray yaml_nodes = Dict_get(self->init, "nodes", EMPTYVAL)._arr_;
    if (add_in)
        ValArray_extend(yaml_nodes, add_in);
    self->draw_layers = Dict_get(self->init, "layers", EMPTYVAL)._arr_;
error:
    self = Scene_delete(self);
    return NULL;
}
Scene Scene_delete(Scene self) {
    if (self) {
        if (self->init) {
            Dict_delete(self->init);
        }
        free(self);
    }
    return NULL;
}
void Scene_update(void);
void Scene_place_node(void);
void Scene_refresh(void);
void Scene_serialize(void);
void Scene_node_by_id(void);
void Scene_node_ids(void);
void Scene_node_in_groups(void);

#ifdef __SCENE_MAIN__
int main() { return 0; }
#endif
#endif
