#ifndef __NODELIST_H__
#define __NODELIST_H__

#include "node.h"
#define kf_pair(k, f)                                                          \
    (KeyFuncPair) { .key = k, .func = f }

typedef struct {
    char *key;
    NodeFunc func;
} KeyFuncPair;

KeyFuncPair SETUP_FUNCS[] = {
    kf_pair("Node", Node_setup),
    kf_pair("Animation", Node_setup),
    kf_pair("Backpack", Node_setup),
    kf_pair("Cactus", Node_setup),
    kf_pair("Camera", Node_setup),
    kf_pair("Coin", Node_setup),
    kf_pair("CutScene", Node_setup),
    kf_pair("Decal", Node_setup), // kf_pair("Decal", Decal_setup),
    kf_pair("Edge", Node_setup),
    kf_pair("Gate", Node_setup),
    kf_pair("Item", Node_setup),
    kf_pair("Menu", Node_setup),
    kf_pair("Music", Node_setup),
    kf_pair("OpenUrlTrigger", Node_setup),
    kf_pair("Retry", Node_setup),
    kf_pair("SFX", Node_setup),
    kf_pair("SoftDirt", Node_setup),
    kf_pair("TextBox", Node_setup),
    kf_pair("TextRoll", Node_setup),
    kf_pair("Trigger", Node_setup)};

size_t SETUP_FUNCS_LENGTH = sizeof(SETUP_FUNCS) / sizeof(KeyFuncPair);
NodeFunc Node_get_setup(char *key);
#endif
