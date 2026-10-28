#include "bitmask.h"

BitMask BitMask_delete(BitMask mask) {
    check(mask, "'mask' is NULL");
    if (mask->data)
        free(mask->data);
    free(mask);
error:
    return NULL;
}

BitMask BitMask_new(uint32_t width, uint32_t height) {
    BitMask mask = NULL;
    mask = (BitMask)malloc(sizeof(struct BitMaskData));
    check_mem(mask);
    uint32_t data_size =
        ((width * height) / sizeof(uint8_t) + 1) * sizeof(uint8_t);
    mask->data = (uint8_t *)malloc(data_size);
    check_mem(mask->data);
    mask->width = width;
    mask->height = height;
    memset(mask->data, 0, data_size);
error:
    return mask;
}

bool BitMask_get(BitMask mask, uint32_t x, uint32_t y) {
    uint32_t index = y * mask->width + x;
    uint32_t byte_index = index / sizeof(uint8_t);
    uint8_t bitnum = index % sizeof(uint8_t);
    uint8_t byte = 0;
    check(index < (mask->width * mask->height), "x = %u, y = %u out of range",
          x, y);
    byte = mask->data[byte_index];
    byte >>= bitnum;
    byte &= 1;

error:
    return (bool)byte;
}

void BitMask_set(BitMask mask, uint32_t x, uint32_t y, bool val) {
    uint32_t index = y * mask->width + x;
    uint32_t byte_index = index / sizeof(uint8_t);
    uint8_t bitnum = index % sizeof(uint8_t);
    uint8_t byte = 0;
    check(index < (mask->width * mask->height), "x = %u, y = %u out of range",
          x, y);
    // debug("x = %lu, y = %lu", x, y);
    byte = mask->data[byte_index];
    if (val)
        byte = byte | (1 << bitnum);
    else
        byte = byte & ~(1 << bitnum);
    mask->data[byte_index] = byte;
error:;
}

BitMask BitMask_from_image(Image img, int threshold) {
    BitMask mask = BitMask_new(img.width, img.height);

    for (int j = 0; j < img.height; j++)
        for (int i = 0; i < img.width; i++)
            if (GetImageColor(img, i, j).a >= threshold)
                BitMask_set(mask, i, j, true);
            else
                BitMask_set(mask, i, j, false);

    return mask;
}

Image BitMask_to_image(BitMask mask, Color set_color, Color unset_color) {
    // start with all zeros
    Image img = GenImageColor(mask->width, mask->height, unset_color);
    for (int j = 0; j < img.height; j++)
        for (int i = 0; i < img.width; i++)
            if (BitMask_get(mask, i, j))
                ImageDrawPixel(&img, i, j, set_color);
    return img;
}

void BitMask_print(BitMask mask) {
    for (int y = 0; y < mask->height; y++) {
        for (int x = 0; x < mask->width; x++) {
            printf(" %u", BitMask_get(mask, x, y));
        }
        printf("\n");
    }
}

bool BitMask_collide(BitMask mask, BitMask other, Vector2 offset) {
    for (int y = 0; y < mask->height; y++)
        for (int x = 0; x < mask->width; x++)
            if (x + offset.x >= 0 && y + offset.y >= 0 &&
                x + offset.x < other->width && y + offset.y < other->height &&
                BitMask_get(mask, x, y) &&
                BitMask_get(other, x + offset.x, y + offset.y))
                return true;
    return false;
} // TODO optimize this

#ifdef __BITMASK_MAIN__

#include <stdio.h>

int main() {
    Image img = LoadImage("./assets/actor/larry/larry_base.png");
    // int width = img.width, height = img.height;
    int width = 32, height = 32;

    BitMask mask = BitMask_from_image(img, DEFAULT_THRESHOLD);
    BitMask_print(mask);
    UnloadImage(img);

    img = BitMask_to_image(mask, WHITE, BLANK);
    mask = BitMask_delete(mask);
    printf("\n");

    mask = BitMask_from_image(img, DEFAULT_THRESHOLD);
    BitMask_print(mask);
    mask = BitMask_delete(mask);
    printf("\n");

    mask = BitMask_new(width, height);
    BitMask_print(mask);
    printf("\n");

    for (int j = 0; j < height; j++) {
        for (int i = 0; i < width; i++) {
            if ((i % 2 == 1 && j % 2 == 1) || (i % 2 == 0 && j % 2 == 0))
                BitMask_set(mask, i, j, true);
        }
    }
    BitMask_print(mask);
    mask = BitMask_delete(mask);
    UnloadImage(img);
    return 0;
}
#endif
