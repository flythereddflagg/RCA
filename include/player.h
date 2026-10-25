#ifndef __PLAYER_H__
#define __PLAYER_H__
#include "dbg.h"
#include <stdlib.h>

typedef struct PlayerData *Player;

void Player_update(const void *self);
void Player_delete(void *self);
Player Player_new();

#endif
