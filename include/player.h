#ifndef __PLAYER_H__
#define __PLAYER_H__
#include "dbg.h"
#include <stdlib.h>

typedef struct PlayerData *Player;

struct PlayerData {
    void *move;
    double speed;
    Vector2 damage_direction;
    Lstring state;
};
Player Player_setup();
Node Player_delete(Node node);
int Player_update(Node node);

#endif
