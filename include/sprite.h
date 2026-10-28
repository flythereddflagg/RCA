#ifndef __SPRITE_H__
#define __SPRITE_H__
#include "dbg.h"
#include "raylib.h"
#include "bitmask.h"
#include <stdlib.h>
typedef struct SpriteData *Sprite;

struct SpriteData {
    Texture2D image;
    BitMask mask;
    Vector2 position;
};
Sprite Sprite_delete(Sprite sprite);
Sprite Sprite_new(char *image_path, Vector2 position);
Texture2D Sprite_set_image(Sprite sprite, Image img);
BitMask Sprite_set_mask(Sprite sprite, BitMask mask);

#endif
