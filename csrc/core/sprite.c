
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

Sprite Sprite_new(char *image_path, Vector2 position) {
    Sprite sprite = (Sprite)malloc(sizeof(struct SpriteData));
    check_mem(sprite);
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
    /*returns the old mask so it can be deleted, null otherwise*/
    check(sprite, "sprite is NULL");
    check(mask, "mask is NULL");
    BitMask to_return = sprite->mask;
    sprite->mask = mask;
    return to_return;
error:
    return NULL;
}
