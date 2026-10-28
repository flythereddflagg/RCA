#ifndef __PLAYER_H__
#define __PLAYER_H__
#include "dbg.h"
#include <stdlib.h>

typedef struct PlayerData *Player;

void Player_update(const void *player);
void Player_delete(void *player);
Player Player_new();

#endif
