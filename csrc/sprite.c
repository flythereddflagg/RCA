
#include "sprite.h"
#include "bitmask.h"

#include "dbg.h"
#include "raylib.h"

#include <stdlib.h>

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

#ifdef __DECAL_MAIN__
int main() { return 0; }
#endif
