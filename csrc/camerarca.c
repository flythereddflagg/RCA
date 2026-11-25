#include "camerarca.h"

int CameraRCA_setup(Node node) {
    check(node, "Node is NULL");
    check(Lstring_equal(node->type, to_Lstring("Camera")),
          "Node->type is '" LSTRING_FMT "', not Camera",
          Lstring_format(node->type));
    node->update = CameraRCA_update;
    node->delete = CameraRCA_delete;
    node->attr = (CameraRCA)malloc(sizeof(struct CameraRCAData));
    check_mem(node->attr);
    CameraRCA camera = (CameraRCA)node->attr;
    camera->mobile_groups = ValArray_new();
    ValArray draw_layers = node->scene->draw_layers;

    for (int i = 0; i < draw_layers->length; i++) {
        if (ValArray_type_at(draw_layers, i) == STR &&
            Lstring_equal(ValArray_get_at(draw_layers, i)._str_,
                          to_Lstring("hud"))) {
            continue;
        }
        ValArray_append(camera->mobile_groups, ValArray_type_at(draw_layers, i),
                        ValArray_get_at(draw_layers, i));
    }
    return 0;
error:
    return -1;
}
int CameraRCA_update(Node node) {
    check(node, "node is NULL");
    check(node->attr, "node->attr is NULL");
    CameraRCA camera = (CameraRCA)node->attr;
    Node player_node = Scene_get_player(node->scene, 0);
    if (!player_node) {
        NodeGroup background =
            (NodeGroup)Dict_get(node->scene->groups, "background", EMPTYVAL)
                ._obj_;
        check(background, "background NodeGroup failed to retreive");
        Vector2 move_vec = ((Node)ObjList_at(background, 0))->sprite->position;
        check(!CameraRCA_pan(node, move_vec), "Pan Failed");
        return 0;
    }
    CameraRCA_follow_player(node);
    if (camera->shaking) {
        // TODO flesh out camera shaking
    }
    if (!Dict_get(node->scene->game->settings, "DEBUG", dynval(_bool_, false))
             ._bool_) {
        CameraRCA_stop_at_border(node);
    }
    return 0;
error:
    return -1;
}
Node CameraRCA_delete(Node node) {
    check(node, "node is NULL");

    CameraRCA camera = (CameraRCA)node->attr;
    if (camera->mobile_groups) {
        int n_layers = camera->mobile_groups->length;
        for (int i = 0; i < n_layers; i++) {
            // this valarray owns none of its elements
            ValArray_remove(camera->mobile_groups, -1);
        }
        camera->mobile_groups = ValArray_delete(camera->mobile_groups);
    }
    if (node->attr) {
        free(node->attr);
        node->attr = NULL;
    }
    node = Node_delete(node);
error:
    return NULL;
}
int CameraRCA_pan(Node node, Vector2 vector) {
    if (!vector.x && !vector.y) {
        return 0;
    }
    check(node, "node is NULL");
    check(node->attr, "node->attr is NULL");
    CameraRCA camera = (CameraRCA)node->attr;
    Vector2 reverse_vector = Vector2Scale(vector, -1.0f);
    NodeGroup group = NULL;
    Lnode current = NULL;
    for (int i = 0; i < camera->mobile_groups->length; i++) {
        group = (NodeGroup)Dict_get(
                    node->scene->groups,
                    camera->mobile_groups->vals[i]._str_.cstring, EMPTYVAL)
                    ._obj_;
        current = group->head;
        for (size_t j = 0; j < group->length; j++) {
            ((Node)current->obj)->sprite->position = Vector2Add(
                ((Node)current->obj)->sprite->position, reverse_vector);
            current = current->next;
        }
    }

    return 0;
error:
    return -1;
}

int CameraRCA_follow_player(Node node) {
    check(node, "node is NULL");
    Node player = Scene_get_player(node->scene, 0);
    check(player, "Player is NULL");
    Vector2 player_center = Vector2Add(
        player->sprite->position, (Vector2){player->sprite->image.width / 2,
                                            player->sprite->image.height / 2});
    Vector2 screen_center =
        (Vector2){node->scene->game->draw_surface.texture.width / 2,
                  node->scene->game->draw_surface.texture.height / 2};
    Vector2 move_xy = Vector2Subtract(player_center, screen_center);
    // move_xy = CameraRCA_add_slack(move_xy, 100.0f);
    CameraRCA_pan(node, move_xy);
    return 0;
error:
    return -1;
}

int CameraRCA_screenshake(Node node, double length, double scale) { return 0; }

Vector2 CameraRCA_add_slack(Vector2 vector, double slack) {
    double movex = vector.x, movey = vector.y;
    double pos_neg = 0;
    if (fabs(movex) > slack) {
        pos_neg = movex > 0.0f ? 1.0f : -1.0f;
        movex = pos_neg * (fabs(movex) - slack);
    } else {
        movex = 0;
    }
    if (fabs(movey) > slack) {
        pos_neg = movey > 0.0f ? 1.0f : -1.0f;
        movex = pos_neg * (fabs(movey) - slack);
    } else {
        movey = 0;
    }

    return (Vector2){movex, movey};
}
int CameraRCA_stop_at_border(Node node) { return 0; }
int CameraRCA_center_player(Node node) { return 0; }
int CameraRCA_zoom_by(Node node, double factor) { return 0; }
int CameraRCA_zoom_abs(Node node, double scale) { return 0; }
