#ifndef __SPRITE_H__
#define __SPRITE_H__
#include "raylib.h"
#include "bitmask.h"

typedef struct SpriteData *Sprite;

Sprite Sprite_delete(Sprite self);
Sprite Sprite_new(char *image_path, Vector2 position);
int Sprite_set_image(Sprite self, Image img);
int Sprite_set_mask(Sprite self, BitMask mask);

#endif
