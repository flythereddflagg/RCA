#include "move.h"

Move Move_new(Sprite sprite, Sprite hitmask_sprite) {
    Move move = (Move)malloc(sizeof(struct MoveData));
    check_mem(move);
    move->sprite = sprite;
    move->hitmask_sprite = hitmask_sprite;
    move->direction = Vector2One();
    return move;
error:
    return NULL;
}
Move Move_delete(Move move) {
    if (move) {
        free(move);
    }
    return NULL;
}
int Move_move(Move move, Vector2 direction, double distance, double speed,
              bool reject_foreground, bool change_direction) {
    check(move, "move is NULL");
    direction = Vector2Normalize(direction);
    direction.y /= 2.0; // for isometric movement
    if (change_direction) {
        move->direction = direction;
    }
    distance += speed * GetFrameTime();
    if (distance < 0) {
        direction = Vector2Scale(direction, -1.0f);
        distance *= -1.0f;
    }
    move->sprite->position =
        Vector2Add(move->sprite->position, Vector2Scale(direction, distance));
    if (move->hitmask_sprite) {
        move->hitmask_sprite->position = Vector2Add(
            move->sprite->position, Vector2Scale(direction, distance));
    }
    if (reject_foreground) {
        check(!Move_foreground_rejection(move, direction, distance),
              "Move_foreground_rejection failed");
    }
    return 0;
error:
    return -1;
}

int Move_foreground_rejection(Move move, Vector2 direction, double distance) {
    check((move && move->sprite && move->sprite->parent &&
           move->sprite->parent->scene->groups),
          "NULL encountered when checking foreground rejection");
    Dict scene_groups = move->sprite->parent->scene->groups;
    if (!Dict_key_in(scene_groups, "solid") || (!direction.x && !direction.y) ||
        (!distance)) {
        return 0;
    }
    Sprite hitmask_sprite =
        move->hitmask_sprite ? move->hitmask_sprite : move->sprite;
    NodeGroup solids =
        (NodeGroup)Dict_get(scene_groups, "solid", EMPTYVAL)._obj_;

    if (!Move_collide_any(move, hitmask_sprite, solids)) {
        return 0;
    }
    double step = distance / 2.0f;
    double tol = 0.005f;
    double mul = 1.0f;

    while (step / distance > tol) {
        mul = Move_collide_any(move, hitmask_sprite, solids) ? -1.0f : 1.0f;
        move->sprite->position = Vector2Add(
            move->sprite->position, Vector2Scale(direction, mul * step));
        if (move->hitmask_sprite) {
            move->hitmask_sprite->position = Vector2Add(
                move->sprite->position, Vector2Scale(direction, mul * step));
        }
        step /= 2.0f;
    }
    return 0;
error:
    return -1;
}

bool Move_collide_any(Move move, Sprite sprite, NodeGroup group) {
    Lnode current = group->head;
    Node node = NULL;
    for (size_t i = 0; i < group->length; i++) {
        check(current, "current Lnode is NULL at postition %lu", i);
        node = (Node)current->obj;
        if (BitMask_collide(
                node->sprite->mask, sprite->mask,
                Vector2Subtract(node->sprite->position, sprite->position))) {
            return true;
        }
        current = current->next;
    }
error:
    return false;
}
