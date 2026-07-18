#include "dbg.h"
#include "engine.c"

#define INIT_PATH "./assets/init.yaml"

int main(int argc, char *argv[]) {
    Game game = Game_new(INIT_PATH);
    int error_state = Game_run(game);
    check(!error_state, "Game exited with error code %d", error_state) error
        : game = Game_delete(game);
    return error_state;
}
