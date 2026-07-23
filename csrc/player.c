#ifndef __PLAYER_C__
#define __PLAYER_C__
#ifndef __MAIN__
#define __MAIN__
#define __PLAYER_MAIN__
#endif
#include "dbg.h"
#include <stdlib.h>

typedef struct PlayerData *Player;

struct PlayerData {
    void (*update)(const void *self);
    void (*delete)(void *self);
};

void Player_update(const void *self) {
    // Player node = (Player) self;
    // statements...
    ;
}

void Player_delete(void *self) { free(self); }

Player Player_new() {
    Player self = (Player)malloc(sizeof(struct PlayerData));
    check_mem(self);

    self->update = &Player_update;
    self->delete = &Player_delete;

error:
    return self;
}
#endif
#ifdef __PLAYER_MAIN__
int main() { return 0; }
#endif
