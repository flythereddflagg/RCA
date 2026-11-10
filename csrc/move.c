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
    if (change_direction) {
        move->direction = direction;
    }
    distance += speed * GetFrameTime();
    if (distance < 0) {
        direction = Vector2Scale(direction, -1.0f);
        distance *= -1;
    }
    move->sprite->position =
        Vector2Add(move->sprite->position, Vector2Scale(direction, distance));
    if (move->hitmask_sprite) {
        move->hitmask_sprite->position = Vector2Add(
            move->sprite->position, Vector2Scale(direction, distance));
    }
    if (reject_foreground) {
        Move_foreground_rejection(move, direction, distance);
    }
    return 0;
error:
    return -1;
}

int Move_foreground_rejection(Move move, Vector2 direction, double distance) {
    return 0;
}
