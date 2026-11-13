#ifndef __SPRITE_H__
#define __SPRITE_H__
typedef struct SpriteData *Sprite;
#include "bitmask.h"
#include "dbg.h"
#include "node.h"
#include "raylib.h"
#include <stdlib.h>

struct SpriteData {
    Node parent;
    Texture2D image;
    BitMask mask;
    Vector2 position;
};
Sprite Sprite_delete(Sprite sprite);
Sprite Sprite_new(char *image_path, Vector2 position, Node parent);
Texture2D Sprite_set_image(Sprite sprite, Image img);
BitMask Sprite_set_mask(Sprite sprite, BitMask mask);

#endif
