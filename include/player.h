#ifndef __PLAYER_H__
#define __PLAYER_H__
#include "dbg.h"
#include "lstring.h"
#include "node.h"
#include "raylib.h"
#include <stdlib.h>
#define DEFAULT_SPEED 130
#define DEFAULT_STATE "idle"

typedef struct PlayerData *Player;

struct PlayerData {
    void *move;
    double speed;
    Vector2 damage_direction;
    Lstring state;
};
int Player_setup(Node node);
Node Player_delete(Node node);
int Player_update(Node node);

#endif
