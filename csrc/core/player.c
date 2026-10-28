
#include "player.h"

typedef struct PlayerData *Player;

struct PlayerData {
    void (*update)(const void *player);
    void (*delete)(void *player);
};

void Player_update(const void *player) {
    // Player node = (Player) player;
    // statements...
    ;
}

void Player_delete(void *player) { free(player); }

Player Player_new() {
    Player player = (Player)malloc(sizeof(struct PlayerData));
    check_mem(player);

    player->update = &Player_update;
    player->delete = &Player_delete;

error:
    return player;
}

#ifdef __PLAYER_MAIN__
int main() { return 0; }
#endif
