
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
    player->move = NULL; // TODO implement move
    player->speed = DEFAULT_SPEED;
    player->damage_direction = (Vector2){0.0, 1.0};
    player->state = to_Lstring(DEFAULT_STATE);
    return 0;
error:
    return -1;
}
Node Player_delete(Node node) {
    check(node, "node is NULL");
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
int Player_apply_input(Node node) {
    check(node, "node is NULL");
    Input game_input = node->scene->game->input;
    check(game_input, "game input is NULL");
    Action action = game_input->actions[0];
    Sprite sprite = Node_child_by_id(node, "sprite")->sprite;
    double movment_dist =
        (1.0f * ((Player)(node->attr))->speed) /
                Dict_get(node->scene->game->settings, "FPS", EMPTYVAL)._int_;
    for (int i = 0; i < MAX_INPUTS; i++) {
        action = game_input->actions[i];
        switch (action.id) {
        case BUTTON_UP:
            sprite->position.y -= movment_dist;
            break;

        case BUTTON_DOWN:
            sprite->position.y += movment_dist;
            break;

        case BUTTON_LEFT:
            sprite->position.x -= movment_dist;
            break;

        case BUTTON_RIGHT:
            sprite->position.x += movment_dist;
            break;

        default:
            break;
        }
    }
    // continue here
    return 0;
error:
    return -1;
}
