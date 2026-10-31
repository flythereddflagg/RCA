
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
    player->rotation = 0.0;
    player->init_scale =
        Dict_get(node->init, "scale", dynval(_float_, 1))._float_;
    player->scale = 1.0;
    player->image_path =
        Dict_get(node->init, "image", dynval(_str_, LSTRING_NULL))._str_;
    player->mask_path =
        Dict_get(node->init, "mask", dynval(_str_, LSTRING_NULL))._str_;
    player->original = NULL; // TODO update this later with image
    node->sprite = Sprite_new(player->image_path.cstring, (Vector2){0.0, 0.0});
    return 0;
    // TODO decide how to compose objects. With just children? Or do we have a
    // separate thing where we make the children out of other Nodes?
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
