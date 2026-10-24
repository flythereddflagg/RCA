#ifndef __NODELIST_H__
#define __NODELIST_H__
#include "node.h"
#define kf_pair(k, f)                                                          \
    (KeyFuncPair) { .key = k, .func = f }

typedef struct {
    char *key;
    NodeFunc func;
} KeyFuncPair;
extern KeyFuncPair SETUP_FUNCS[];
extern size_t SETUP_FUNCS_LENGTH;

#endif
