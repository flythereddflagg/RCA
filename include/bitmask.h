#ifndef __BITMASK_H__
#define __BITMASK_H__

#include "dbg.h"

#include "raylib.h"
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#define DEFAULT_THRESHOLD 128

typedef struct BitMaskData *BitMask;

struct BitMaskData {
    uint32_t width;
    uint32_t height;
    uint8_t *data;
};

BitMask BitMask_delete(BitMask self);
BitMask BitMask_new(uint32_t width, uint32_t height);
bool BitMask_get(BitMask self, uint32_t x, uint32_t y);
void BitMask_set(BitMask self, uint32_t x, uint32_t y, bool val);
BitMask BitMask_from_image(Image img, int threshold);
Image BitMask_to_image(BitMask mask, Color set_color, Color unset_color);
void BitMask_print(BitMask self);
bool BitMask_collide(BitMask self, BitMask other, Vector2 offset);

#endif
