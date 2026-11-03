
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
    Lstring img_path =
        Dict_get(node->init, "image", dynval(_str_, LSTRING_NULL))._str_;
    node->sprite = Sprite_new(img_path.cstring, (Vector2){0.0, 0.0});
    // TODO add mask
    debug("groups %s", Dict_get(node->init, "groups", EMPTYVAL)._str_.cstring);
    return 0;
error:
    return -1;
}
Node Player_delete(Node node) {
    check(node, "node is NULL");
    if (node->sprite) {
        node->sprite = Sprite_delete(node->sprite);
    }
    if (node->attr) {
        free(node->attr);
        node->attr = NULL;
    }
    node = Node_delete(node);
error:
    return NULL;
}
int Player_update(Node node) { return 0; }
