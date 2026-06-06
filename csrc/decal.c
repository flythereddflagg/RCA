#ifndef __DECAL_C__
#define __DECAL_C__
#include <stdlib.h>
#include "dbg.h"
#include "raylib.h"

typedef struct DecalData* Decal;

struct DecalData{
    void (*delete)(Decal self);
    Texture2D image;
    Vector2 position;
};

void Decal_delete(Decal self){
    check(self, "'self' is NULL");
    UnloadTexture(self->image);
    free(self);
error:
    ;
}

Decal Decal_new(char *image_path, Vector2 position){
    Decal self = (Decal) malloc (sizeof(struct DecalData));
    check_mem(self);

    self->delete = &Decal_delete;
    self->image = LoadTexture(image_path);
    self->position = position;

error:
    return self;
}
#endif