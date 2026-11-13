
#include "player.h"

int Player_setup(Node node) {
    check(node, "Node is NULL");
    check(Lstring_equal(node->type, to_Lstring("Player")),
          "Node->type is '" LSTRING_FMT "', not Player",
          Lstring_format(node->type));
    // check(node->sprite, "Node sprite is NULL");
    node->update = Player_update;
    node->delete = Player_delete;
    node->attr = (Player)malloc(sizeof(struct PlayerData));
    check_mem(node->attr);
    Player player = (Player)node->attr;
    player->move = Move_new(Node_child_by_id(node, "sprite")->sprite, NULL);
    player->speed = DEFAULT_SPEED;
    player->damage_direction = (Vector2){0.0, 1.0};
    player->state = to_Lstring(DEFAULT_STATE);
    return 0;
error:
    return -1;
}
Node Player_delete(Node node) {
    check(node, "node is NULL");
    Player player = (Player)node->attr;
    if (player->move) {
        player->move = Move_delete(player->move);
    }
    if (node->attr) {
        free(node->attr);
        node->attr = NULL;
    }
    node = Node_delete(node);
error:
    return NULL;
}
int Player_update(Node node) {
    check(!Player_apply_input(node), "Apply input failed");

    return 0;
error:
    return -1;
}

#define direction_button_case(_button_, _dir_, _oper_)                         \
    case _button_:                                                             \
        movement_direction._dir_ = movement_direction._dir_ _oper_ action.val; \
        break
int Player_apply_input(Node node) {
    Player player = (Player)(node->attr);
    check(node, "node is NULL");
    Input game_input = node->scene->game->input;
    check(game_input, "game input is NULL");
    Action action = game_input->actions[0];
    Vector2 movement_direction = Vector2Zero();
    for (int i = 0; i < MAX_INPUTS; i++) {
        action = game_input->actions[i];
        switch (action.id) {
            direction_button_case(BUTTON_UP, y, -);
            direction_button_case(BUTTON_DOWN, y, +);
            direction_button_case(BUTTON_LEFT, x, -);
            direction_button_case(BUTTON_RIGHT, x, +);
        default:
            break;
        }
    }
    check(!Move_move(player->move, movement_direction, 0.0,
                     1.0f * player->speed, true, true),
          "Player Move failed");
    return 0;
error:
    return -1;
}
#undef direction_button_case