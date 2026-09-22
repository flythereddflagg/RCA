#ifndef __DECAL_C__
#define __DECAL_C__
#ifndef __MAIN__
#define __MAIN__
#define __DECAL_MAIN__
#endif
#include "bitmask.c"

#include "core.h"
#include "raylib.h"

#include <stdlib.h>

typedef struct SpriteData *Sprite;

struct SpriteData {
    Texture2D image;
    BitMask mask;
    Vector2 position;
};

Sprite Sprite_delete(Sprite self) {
    check(self, "'self' is NULL");
    UnloadTexture(self->image);
    if (self->mask) {
        BitMask_delete(self->mask);
    }
    free(self);
error:
    return NULL;
}

Sprite Sprite_new(char *image_path, Vector2 position) {
    Sprite self = (Sprite)malloc(sizeof(struct SpriteData));
    check_mem(self);
    self->image = LoadTexture(image_path);
    self->mask = NULL;
    self->position = position;

error:
    return self;
}

int Sprite_set_image(Sprite self, Image img) { return 0; }

int Sprite_set_mask(Sprite self, BitMask mask) { return 0; }

#endif
#ifdef __DECAL_MAIN__
int main() { return 0; }
#endif
