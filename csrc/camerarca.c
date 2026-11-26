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
    Vector2 player_center =
        Vector2Add(player->sprite->position,
                   (Vector2){player->sprite->image.width / 2.0f,
                             player->sprite->image.height / 2.0f});
    Vector2 move_xy =
        Vector2Subtract(player_center, Game_get_center(node->scene->game));
    move_xy = CameraRCA_add_slack(move_xy, 100.0f);
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
        movex = 0.0f;
    }
    if (fabs(movey) > (slack / 2.0)) {
        pos_neg = movey > 0.0f ? 1.0f : -1.0f;
        movey = pos_neg * (fabs(movey) - (slack / 2.0));
    } else {
        movey = 0.0f;
    }

    return (Vector2){movex, movey};
}
int CameraRCA_stop_at_border(Node node) {
    check(node, "node is NULL");
    double screen_w = node->scene->game->draw_surface.texture.width;
    double screen_h = node->scene->game->draw_surface.texture.height;
    Node bg_ref = Scene_get_background(node->scene);
    check(bg_ref, "retreiving background node failed");
    double background_w = bg_ref->sprite->image.width;
    double background_h = bg_ref->sprite->image.height;
    // if background is smaller than screen size, center it in the frame and
    // do not do anything else
    if (background_w < screen_w || background_h < screen_h) {
        Vector2 move_xy = Vector2Subtract(bg_ref->sprite->position,
                                          Game_get_center(node->scene->game));
        check(!CameraRCA_pan(node, move_xy), "pan failed");
        return 0;
    }

    Vector2 back_xy = Vector2Zero();
    if (bg_ref->sprite->position.x > 0) {
        back_xy.x = bg_ref->sprite->position.x;
    } else if (bg_ref->sprite->position.x + background_w < screen_w) {
        back_xy.x = bg_ref->sprite->position.x + background_w - screen_w;
    }

    if (bg_ref->sprite->position.y > 0) {
        back_xy.y = bg_ref->sprite->position.y;
    } else if (bg_ref->sprite->position.y + background_h < screen_h) {
        back_xy.y = bg_ref->sprite->position.y + background_h - screen_h;
    }
    check(!CameraRCA_pan(node, back_xy), "pan failed");
    return 0;
error:
    return -1;
}


// TODO add logic that pans camera infront of where the player is looking.
