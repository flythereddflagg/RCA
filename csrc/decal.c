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

typedef struct DecalData *Decal;

struct DecalData {
    Texture2D image;
    BitMask mask;
    Vector2 position;
};

Decal Decal_delete(Decal self) {
    check(self, "'self' is NULL");
    UnloadTexture(self->image);
    if (self->mask) {
        BitMask_delete(self->mask);
    }
    free(self);
error:
    return NULL;
}

Decal Decal_new(char *image_path, Vector2 position) {
    Decal self = (Decal)malloc(sizeof(struct DecalData));
    check_mem(self);
    self->image = LoadTexture(image_path);
    self->mask = NULL;
    self->position = position;

error:
    return self;
}

int Decal_set_image(Decal self, Image img) { return 0; }

int Decal_set_mask(Decal self, BitMask mask) { return 0; }

#endif
#ifdef __DECAL_MAIN__
int main() { return 0; }
#endif
