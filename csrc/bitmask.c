#ifndef __BITMASK_C__
#define __BITMASK_C__
#include "dbg.h"
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

typedef struct BitMaskData *BitMask;

struct BitMaskData {
    uint64_t width;
    uint64_t height;
    uint8_t *data;
};

void BitMask_delete(BitMask self) {
    check(self, "'self' is NULL");
    if (self->data)
        free(self->data);
    free(self);
error:;
}

BitMask BitMask_new(uint64_t width, uint64_t height) {
    BitMask self = (BitMask) malloc(sizeof(struct BitMaskData));
    check_mem(self);
    self->data = (uint8_t*) malloc(
        ((width * height) / sizeof(uint8_t) + 1) * sizeof(uint8_t));
    self->width = width;
    self->height = height;
    memset(self->data, 0, (width * height) / 8 + 1);
error:
    return self;
}

bool BitMask_get(BitMask self, uint64_t i, uint64_t j){
    uint64_t index = i * self->height + j;
    uint8_t bitnum = index % sizeof(uint8_t);
    uint8_t byte = 0;
    check(
        index < (self->width * self->height), 
        "i = %lu, j = %lu out of range", i, j);
    byte = self->data[index / sizeof(uint8_t)];
    byte >>= bitnum;
    byte &= 1;

error:
    return (bool) byte;
}

void BitMask_set(BitMask self, uint64_t i, uint64_t j, bool val){
    uint64_t index = i * self->height + j;
    uint8_t bitnum = index % sizeof(uint8_t);
    uint8_t byte = 0;
    check(
        index < (self->width * self->height), 
        "i = %lu, j = %lu out of range", i, j);
    // debug("i = %lu, j = %lu", i, j);
    byte = self->data[index / sizeof(uint8_t)];
    if (val)
        self->data[index] = byte | (1 << bitnum);
    else
        self->data[index] = byte & ~(1 << bitnum);
error:;
}

BitMask BitMask_from_image(Image img, int threshold){
    BitMask mask = BitMask_new(img.width, img.height);
    
    for(int j = 0; j < img.height; j++)
        for(int i = 0; i < img.width; i++)
            if (GetImageColor(img, i, j)[3] > threshold)
                BitMask_set(mask, i, j, true);
    
    return mask;// TODO Test this
}

#endif
#ifdef TEST_MAIN
#include <stdio.h>

int main(){
    Image img = LoadImage("./assets/actor/larry/larry_base.png");
    int width = img.width, height = img.height;


    BitMask mask = BitMask_new(width, height);
    for (int j = 0; j < height; j++){
        for (int i = 0; i < width; i++){
            if ((i % 2 && j % 2) || (!(i % 2) && !(j % 2)))
                BitMask_set(mask, i, j, true);
        }
    }
    for (int j = 0; j < height; j++){
        for (int i = 0; i < width; i++){
            printf("%u", BitMask_get(mask, i, j));
        }
        printf("\n");
    }
    BitMask_delete(mask);
    ImageUnload(img);
    return 0;
}
#endif
