#ifndef __SCENE_C__
#define __SCENE_C__
#ifndef __MAIN__
#define __MAIN__
#define __SCENE_MAIN__
#endif
#include "core.h"
#include "dict.c"
#include "engine.c"
#include "lstring.c"
#include "node.c"
#include "valarray.c"
#include <stdbool.h>
#define BG_REF "bg_ref"

// TODO implement Scene logic
Scene Scene_delete(Scene);
int Scene_place_node(Scene scene, Node node, ValArray groups, Vector2 start,
                     bool active);
void Scene_update(void);
void Scene_refresh(void);
void Scene_serialize(void);
void Scene_node_by_id(void);
void Scene_node_ids(void);
void Scene_node_in_groups(void);

struct SceneData {
    Game game;
    bool paused;
    bool occupied;
    Lstring id;
    Dict init;
    ValArray draw_layers;
    Dict groups; // dict of NodeGroup
    NodeGroup all_nodes;
    NodeGroup active_nodes;
    // Node bg_ref;
};
Scene Scene_new(Game game, char *yaml_path, Dict yaml_data, ValArray add_in) {
    Scene self = (Scene)malloc(sizeof(struct SceneData));
    check_mem(self);
    self->game = game;
    self->paused = false;
    self->occupied = false;
    self->id = Lstring_new(yaml_path);
    self->init =
        yaml_data ? yaml_data : YamlParse_process_yaml_file(yaml_path)._dict_;
    self->draw_layers = Dict_get(self->init, "layers", EMPTYVAL)._arr_;
    self->groups = Dict_new();
    self->all_nodes = NodeGroup_new("all_nodes");
    self->active_nodes = NodeGroup_new("active_nodes");
    // self->bg_ref = NULL;
    ValArray yaml_nodes = Dict_get(self->init, "nodes", EMPTYVAL)._arr_;
    if (add_in)
        ValArray_extend(yaml_nodes, add_in);

    // guarentee background exists
    bool add_background_blank = false;
    if (!ValArray_string_in(self->draw_layers, "background")) {
        add_background_blank = true;
        ValArray_insert(self->draw_layers, 0, STR,
                        dynval(_str_, Lstring_new("background")));
    }
    // guarentee hud exists and is drawn last
    if (!ValArray_string_in(self->draw_layers, "hud")) {
        ValArray_append(self->draw_layers, STR,
                        dynval(_str_, Lstring_new("hud")));
    }
    // guarentee a blank background sprite if none exists.
    if (add_background_blank)
        
        Scene_place_node(scene, Node_new());

    return self;
error:
    self = Scene_delete(self);
    return NULL;
}
Scene Scene_delete(Scene self) {
    if (self) {
        self->active_nodes = NodeGroup_delete(self->active_nodes);
        self->all_nodes = NodeGroup_delete(self->all_nodes);
        self->groups = Dict_delete(self->groups);
        self->init = Dict_delete(self->init);
        self->id = Lstring_delete(self->id);
        free(self);
    }
    return NULL;
}

int Scene_place_node(Scene scene, Node node, ValArray groups, Vector2 start,
                     bool active) {
    node->scene = scene;
    NodeGroup_add(scene->all_nodes, node);
    if (active)
        NodeGroup_add(scene->active_nodes, node);
    Node child = NULL;
    ValArray startvec = NULL;
    for (int i = 0; i < node->children->length; i++) {
        child = (Node)ValArray_get_at(node->children, i)._obj_;
        startvec = Dict_get(child->init, "start", EMPTYVAL)._arr_;
        Scene_place_node(
            scene, child, Dict_get(child->init, "groups", EMPTYVAL)._arr_,
            startvec ? (Vector2){ValArray_get_at(startvec, 0)._float_,
                                 ValArray_get_at(startvec, 1)._float_}
                     : (Vector2){0.0, 0.0},
            Dict_get(child->init, "active", dynval(_bool_, active))._bool_);
    }
    if (node->sprite == NULL){
        if (groups){
            // TODO continue here
        }
    }
    return 0;
}

#ifdef __SCENE_MAIN__
int main() {
    Scene scene = Scene_new(NULL, "./assets/scene/startup.yaml", NULL, NULL);

    scene = Scene_delete(scene);
    return 0;
}
#endif
#endif
