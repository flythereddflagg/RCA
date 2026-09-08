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
Scene Scene_new(Game game, char *yaml_path, Dict yaml_data, ValArray add_in) {
    Scene self = (Scene)malloc(sizeof(struct SceneData));
    check_mem(self);
    self->game = game;
    self->paused = false;
    self->id = Lstring_new(yaml_path);
    self->init =
        yaml_data ? yaml_data : YamlParse_process_yaml_file(yaml_path)._dict_;
    ValArray yaml_nodes = Dict_get(self->init, "nodes", EMPTYVAL)._arr_;
    if (add_in)
        ValArray_extend(yaml_nodes, add_in);
    self->draw_layers = Dict_get(self->init, "layers", EMPTYVAL)._arr_;
    // guarentee background exists
    bool add_background_blank = false;
    for (int i = 0; i < self->draw_layers->length; i++) {
        if (STR != ValArray_type_at(self->draw_layers, i))
            continue;
        if (Lstring_cstring_equal(
                ValArray_get_at(self->draw_layers, i)._str_.cstring,
                "background")) {
            add_background_blank = true;
            ValArray_insert(self->draw_layers, 0, STR,
                            dynval(_str_, Lstring_new("background")));
            break;
        }
    }

    return self;
error:
    self = Scene_delete(self);
    return NULL;
}
Scene Scene_delete(Scene self) {
    if (self) {
        self->init = Dict_delete(self->init);
        self->id = Lstring_delete(self->id);
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
int main() {
    Scene scene = Scene_new(NULL, "./assets/scene/startup.yaml", NULL, NULL);
    debug("%p", scene->init);
    Dict_print(scene->init);
    debug("Testing insert");
    ValArray_print(scene->draw_layers);
    printf("\n");
    scene = Scene_delete(scene);
    return 0;
}
#endif
#endif
