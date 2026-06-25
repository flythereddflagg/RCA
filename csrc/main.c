#include "dbg.h"
#include "engine.c"

#define INIT_PATH "./assets/init.yaml"

int main(int argc, char *argv[]){
    Game game = Game_new(INIT_PATH);
    int error_state = Game_run(game);
    Game_delete(game);
    return error_state;
}