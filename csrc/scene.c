#ifndef __SCENE_C__
#define __SCENE_C__
#ifndef __MAIN__
#define __MAIN__
#define __SCENE_MAIN__
#endif
#include "dictarr.c"
#include "lstring.c"
#include "node.c"
#include <stdbool.h>

// TODO implement Scene logic

typedef struct SceneData *Scene;
struct SceneData {
    Game game;
    bool paused;
    bool occupied;
    Lstring id;
    Lstring *draw_layers;
    Lstring *group_names;
    NodeArray *groups;
    NodeArray all_nodes;
    NodeArray active_nodes;
    Node bg_ref;
    Dict init;
};
Scene Scene_new(Game game, Lstring yaml_path, Dict yaml_data, Dict add_in) {
    Scene self = (Scene)malloc(sizeof(struct SceneData));
    self->game = game;
    self->paused = false;
    self->id = yaml_path;
    self->init = yaml_data
                     ? yaml_data
                     : YamlParse_process_yaml_file(yaml_path.cstring)._dict_;

    return NULL;
}
void Scene_delete(void);
void Scene_update(void);
void Scene_place_node(void);
void Scene_refresh(void);
void Scene_serialize(void);
void Scene_node_by_id(void);
void Scene_node_ids(void);
void Scene_node_in_groups(void);

#endif
#ifdef __SCENE_MAIN__
int main() { return 0; }
#endif
