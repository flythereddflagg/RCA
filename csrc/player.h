#ifndef __PLAYER_H__
#define __PLAYER_H__

typedef struct PlayerData *Player;

void Player_update(const void *self);
void Player_delete(void *self);
Player Player_new();

#endif
