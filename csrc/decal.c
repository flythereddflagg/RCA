
#include "decal.h"
int Decal_setup(Node node) {
    check(node, "Node is NULL");
    check(Lstring_equal(node->type, to_Lstring("Decal")),
          "Node->type is '" LSTRING_FMT "', not Decal",
          Lstring_format(node->type));
    check(node->sprite, "Node sprite is NULL");
    node->update = Decal_update;
    node->delete = Decal_delete;
    node->attr = (Decal)malloc(sizeof(struct DecalData));
    check_mem(node->attr);
    Decal decal = (Decal)node->attr;
    decal->rotation = 0.0;
    decal->init_scale =
        Dict_get(node->init, "scale", dynval(_float_, 1))._float_;
    decal->scale = 1.0;
    decal->image_path =
        Dict_get(node->init, "image", dynval(_str_, LSTRING_NULL))._str_;
    decal->mask_path =
        Dict_get(node->init, "mask", dynval(_str_, LSTRING_NULL))._str_;
    decal->original = NULL; // TODO update this later with image
    node->sprite = Sprite_new(decal->image_path.cstring, (Vector2){0.0, 0.0});
    return 0;
error:
    return -1;
}
Node Decal_delete(Node node) {
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
int Decal_update(Node node) { return 0; }
