#ifndef __SCENE_C__
#define __SCENE_C__
#ifndef __MAIN__
#define __MAIN__
#define __SCENE_MAIN__
#endif
#include "core.h"
#include "dict.c"
#include "lstring.c"
#include "node.c"
#include "valarray.c"
#include "yaml_parse.c"
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
    DynValue bg_vals[] = {dynval(_str_, to_Lstring("background"))};
    DynType bg_types[] = {STR};
    struct ValArrayData bg_gp_list =
        (struct ValArrayData){.length = (int)sizeof(bg_vals) / sizeof(DynValue),
                              .vals = (DynValue *)&(bg_vals[0]),
                              .types = (DynType *)&(bg_types[0])};

    Scene scene = (Scene)malloc(sizeof(struct SceneData));
    check_mem(scene);
    scene->game = game;
    scene->paused = false;
    scene->occupied = false;
    scene->id = Lstring_new(yaml_path);
    scene->init =
        yaml_data ? yaml_data : YamlParse_process_yaml_file(yaml_path)._dict_;
    scene->draw_layers = Dict_get(scene->init, "layers", EMPTYVAL)._arr_;
    scene->groups = Dict_new();
    scene->all_nodes = NodeGroup_new("all_nodes");
    scene->active_nodes = NodeGroup_new("active_nodes");
    // scene->bg_ref = NULL;
    ValArray yaml_nodes = Dict_get(scene->init, "nodes", EMPTYVAL)._arr_;
    if (add_in)
        ValArray_extend(yaml_nodes, add_in);

    // guarentee background exists
    bool add_background_blank = false;
    if (!ValArray_string_in(scene->draw_layers, "background")) {
        add_background_blank = true;
        ValArray_insert(scene->draw_layers, 0, STR,
                        dynval(_str_, Lstring_new("background")));
    }
    // guarentee hud exists and is drawn last if not explicitly placed
    if (!ValArray_string_in(scene->draw_layers, "hud")) {
        ValArray_append(scene->draw_layers, STR,
                        dynval(_str_, Lstring_new("hud")));
    }
    // guarentee a blank background sprite if none exists.
    if (add_background_blank) {
        // Scene_place_node(scene, Node_new(), (ValArray)&bg_gp_list, NULL,
        // false);
    }
    ValArray node_list = Dict_get(scene->init, "nodes", EMPTYVAL)._arr_;
    Node current = NULL;
    check(node_list, "node list did not load");
    for (int i = 0; i < node_list->length; i++) {
        current = Node_from_dict(ValArray_get_at(node_list, i)._dict_);
        check(current, "current NODE is NULL");
        current->delete(current);
        // Scene_place_node(
        //     scene, current, Dict_get(current->init, "groups",
        //     EMPTYVAL)._arr_, Dict_get(current->init, "start",
        //     EMPTYVAL)._arr_, Dict_get(current->init, "active", dynval(_bool_,
        //     true))._bool_);
    }

    return scene;
error:
    scene = Scene_delete(scene);
    return NULL;
}
Scene Scene_delete(Scene scene) {
    if (scene) {
        scene->active_nodes = NodeGroup_delete(scene->active_nodes);
        scene->all_nodes = NodeGroup_delete(scene->all_nodes);
        scene->groups = Dict_delete(scene->groups);
        scene->init = Dict_delete(scene->init);
        scene->id = Lstring_delete(scene->id);
        free(scene);
    }
    return NULL;
}

int Scene_place_node(Scene scene, Node node, ValArray groups, ValArray start,
                     bool active) {
    check(scene, "scene is NULL");
    check(node, "node is NULL");
    node->scene = scene;
    NodeGroup_add(scene->all_nodes, node);
    if (active)
        NodeGroup_add(scene->active_nodes, node);
    Node child = NULL;
    Vector2 startvec = start ? (Vector2){ValArray_get_at(start, 0)._float_,
                                         ValArray_get_at(start, 1)._float_}
                             : (Vector2){0.0, 0.0};
    for (int i = 0; i < node->children->length; i++) {
        child = (Node)ValArray_get_at(node->children, i)._obj_;
        Scene_place_node(
            scene, child, Dict_get(child->init, "groups", EMPTYVAL)._arr_,
            Dict_get(child->init, "start", EMPTYVAL)._arr_,
            Dict_get(child->init, "active", dynval(_bool_, active))._bool_);
    }

    if (groups) {
        NodeGroup nd_grp = NULL;
        Lstring cur_grp = LSTRING_NULL;
        for (int i = 0; i < groups->length; i++) {
            // groups is a ValArray of strings
            if (!Dict_key_in(scene->groups,
                             ValArray_get_at(groups, i)._str_.cstring)) {
                cur_grp = ValArray_get_at(groups, i)._str_;
                Dict_set(scene->groups, cur_grp.cstring, OBJ,
                         dynval(_obj_, NodeGroup_new(cur_grp.cstring)));
            }
            nd_grp = (NodeGroup)Dict_get(
                         scene->groups,
                         ValArray_get_at(groups, i)._str_.cstring, EMPTYVAL)
                         ._obj_;
            NodeGroup_add(nd_grp, node);
        }
    }
    if (start) {
        check(node->sprite, "No  to set start vector");
        node->sprite->position = startvec;
    }

    return 0;
error:
    return -1;
}

int Scene_update(Scene scene) {
    check(scene, "Scene is null");
    if (scene->paused) {
        NodeGroup pause_group =
            (NodeGroup)Dict_get(scene->groups, "paused", EMPTYVAL)._obj_;
        check(pause_group, "pause group is NULL");
        check(!NodeGroup_update(pause_group), "pause group update failed.");
    } else {
        check(scene->active_nodes, "pause group is NULL");
        check(!NodeGroup_update(scene->active_nodes),
              "active node update failed.");
    }
    return 0;
error:
    return -1;
}

Node Scene_node_by_id(Scene scene, char *node_id) {
    Node node = NULL;
    Lstring id_str = LSTRING_NULL;
    check(scene, "scene is NULL");
    check(node_id, "node id is NULL");
    id_str = Lstring_new(node_id);
    for (int i = 0; i < scene->active_nodes->length; i++) {
        node = (Node)ValArray_get_at(scene->active_nodes, i)._obj_;
        if (node && Lstring_equal(id_str, node->id))
            break;
        else
            node = NULL;
    }
error:
    id_str = Lstring_delete(id_str);
    return node;
}

#ifdef __SCENE_MAIN__
int main() {
    Scene scene = Scene_new(NULL, "./assets/scene/startup.yaml", NULL, NULL);
    // Dict_print(scene->init);
    scene = Scene_delete(scene);
    return 0;
}
#endif
#endif
