#ifndef MOVE_H
#define MOVE_H
#include "raylib.h"
#include "raymath.h"
#include "sprite.h"
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>
typedef struct MoveData *Move;

struct MoveData {
    Sprite sprite;
    Sprite hitmask_sprite;
    Vector2 direction;
};

Move Move_new();
Move Move_delete(Move move);
int Move_move(Move move, Vector2 direction, double distance, double speed,
              bool reject_foreground, bool change_direction);

int Move_foreground_rejection(Move move, Vector2 direction, double distance);

#endif
