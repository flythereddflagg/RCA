#ifndef __PLAYER_H__
#define __PLAYER_H__
#include <stdlib.h>
#include "dbg.h"

typedef struct PlayerData *Player;

void Player_update(const void *self);
void Player_delete(void *self);
Player Player_new();

#endif
