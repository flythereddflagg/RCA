
#include "sprite.h"

Sprite Sprite_delete(Sprite sprite) {
    check(sprite, "'sprite' is NULL");
    UnloadTexture(sprite->image);
    if (sprite->mask) {
        BitMask_delete(sprite->mask);
    }
    free(sprite);
error:
    return NULL;
}

Sprite Sprite_new(char *image_path, Vector2 position, Node parent) {
    Sprite sprite = (Sprite)malloc(sizeof(struct SpriteData));
    check_mem(sprite);
    debug("image path: %s", image_path);
    sprite->parent = parent;
    sprite->image = LoadTexture(image_path);
    sprite->mask = NULL;
    sprite->position = position;

error:
    return sprite;
}

Texture2D Sprite_set_image(Sprite sprite, Image img) {
    /*returns the old image so it can be deleted, null otherwise*/
    check(sprite, "sprite is NULL");
    check(img.data, "Image is invalid");
    Texture2D to_return = sprite->image;
    sprite->image = LoadTextureFromImage(img);
    check(IsTextureValid(sprite->image), "Invalid image loaded");
    return to_return;
error:
    return (Texture2D){
        .id = 0, .width = 0, .height = 0, .mipmaps = 0, .format = 0};
}

BitMask Sprite_set_mask(Sprite sprite, BitMask mask) {
    /*returns the old mask so it can be deleted, null on error*/
    check(sprite, "sprite is NULL");
    check(mask, "mask is NULL");
    BitMask to_return = sprite->mask;
    sprite->mask = mask;
    return to_return;
error:
    return NULL;
}

bool Sprite_collide_any(Sprite sprite, NodeGroup group) {
    Lnode current = group->head;
    Node node = NULL;
    for (size_t i = 0; i < group->length; i++) {
        check(current, "current Lnode is NULL at postition %lu", i);
        node = (Node)current->obj;
        if (BitMask_collide(
                node->sprite->mask, sprite->mask,
                Vector2Subtract(node->sprite->position, sprite->position))) {
            return true;
        }
        current = current->next;
    }
error:
    return false;
}
