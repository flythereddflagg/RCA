#ifndef DECAL_H
#define DECAL_H
#include "lstring.h"
#include "node.h"
#include "dict.h"
#include "sprite.h"
#include <stdlib.h>
#include "raylib.h"

typedef struct DecalData *Decal;

struct DecalData {
    double rotation;
    double init_scale;
    double scale;
    Lstring image_path;
    Lstring mask_path;
    Sprite original;
};

int Decal_setup(Node node);
Node Decal_delete(Node node);
int Decal_update(Node node);

#endif
