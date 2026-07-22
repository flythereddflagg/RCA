#ifndef __DICT_C__
#define __DICT_C__
#ifndef __MAIN__
#define __MAIN__
#define __DICT_MAIN__
#endif
#include "dbg.h"
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#define DICTKEYLENGTH 256
#define DICTSIZE 255
#define HASHPRIME 31
#define NO_NEXT -1
#define EMPTYVAL                                                               \
    (DictVal) { ._obj_ = NULL }

typedef struct DictData *Dict;
typedef union DictValData DictVal;
typedef char *DictKey;
typedef enum { NONE, DICT, ARR, STR, INT, FLOAT, BOOL, OBJ } DictType;

union DictValData {
    Dict _dict_;
    DictVal *_arr_;
    char *_str_;
    int _int_;
    float _float_;
    bool _bool_;
    void *_obj_;
    // NULL none;
};

struct DictData {
    DictKey *keys;
    DictType *types;
    DictVal *vals;
    int *next;
};

int Dict_hash(const DictKey key) {
    long long hash = 0, hpow = 1;
    int i = 0;
    for (i = 0; i < DICTKEYLENGTH; i++) {
        if (key[i] == '\0')
            break;
        hpow = 1;
        for (int j = 0; j < i + 1; j++)
            hpow *= key[i];
        hash += hpow * HASHPRIME;
    }
    check(i > 0, "invalid hash key");
    // debug("hash %lld", hash);
    return hash % DICTSIZE;

error:
    return -1;
}

int Dict_set(Dict self, DictKey key, DictType type, DictVal val) {
    check(self, "invalid dict supplied");
    check(key[0], "invalid key supplied");
    // get the hash value
    int hash_i = Dict_hash(key), index = 0, i = 0;

    // if the key at that index is not empty follow the linked list to the end
    while (self->keys[index] && self->next[hash_i] != NO_NEXT)
        hash_i = self->next[hash_i];

    index = hash_i;
    // now we have the end of the current hash list
    // so we increment by 1 until we either find an empty slot or the given key
    for (i = 0; i < DICTSIZE; i++) {
        if (!self->keys[index] ||
            !strncmp(key, self->keys[index], DICTKEYLENGTH))
            break;
        index++;
        // wrap around
        if (index >= DICTSIZE)
            index -= DICTSIZE;
    }
    check(i < DICTSIZE, "Dict is full");
    // then if we needed to find another slot, we link to it in the previous one
    if (hash_i != index)
        self->next[hash_i] = index;

    check(index >= 0 && index < DICTSIZE, "invalid index detected");
    self->keys[index] = key;
    self->types[index] = type;
    self->vals[index] = val;
    return 0;
error:
    return -1;
}

int Dict_delkey(Dict self, DictKey key) {
    check(self, "invalid dict supplied");
    check(key[0], "invalid key supplied");
    int prev = Dict_hash(key), index = prev;
    debug("%s", key);
    debug("%d", index);
    // TODO figure out how to represent this
    // if keys do not match follow the linked list and error if we reach the end
    while (!self->keys[index] ||
           strncmp(key, self->keys[index], DICTKEYLENGTH)) {
        debug("%d", index);
        check(self->next[index] != NO_NEXT, "'%s' Key not found", key);
        prev = index;
        index = self->next[index];
    }

    // we now have the index which we erase saving the 'next' value
    int tmp_next = self->next[index];
    self->keys[index] = NULL;
    self->next[index] = NO_NEXT;
    // then we set the prev item to be the next
    self->next[prev] = tmp_next;
    return 0;
error:
    return -1;
}

DictVal Dict_get(Dict self, DictKey key, DictVal _default) {
    check(self, "invalid dict supplied");
    check(key[0], "invalid key supplied");
    int index = Dict_hash(key);
    while (!self->keys[index] ||
           strncmp(key, self->keys[index], DICTKEYLENGTH)) {
        check(self->next[index] != NO_NEXT, "'%s' Key not found", key);
        index = self->next[index];
    }
    return self->vals[index];

error:
    return EMPTYVAL;
}

void Dict_printrepr(Dict dict) {

    printf("\n[ind]        key |  type                  val | next\n");
    printf("----------------------------------------------------\n");

    for (int i = 0; i < DICTSIZE; i++) {
        if (!dict->keys[i] || !dict->keys[i][0])
            continue;
        printf("[%3d] %10s | ", i, dict->keys[i]);
        switch (dict->types[i]) {
        case NONE:
            printf(" none %20s", "null");
            break;
        case DICT:
            Dict_printrepr(dict->vals[i]._dict_);
            break;
        case ARR:
        case STR:
            printf("  str %20s", dict->vals[i]._str_);
            break;
        case INT:
            printf("  int %20d", dict->vals[i]._int_);
            break;
        case FLOAT:
            printf("float %20f", dict->vals[i]._float_);
            break;
        case BOOL:
            printf(" bool %20d", dict->vals[i]._bool_);
            break;
        case OBJ:
            printf("  obj %20p", dict->vals[i]._obj_);
            break;
        default:
            sentinel("invalid type") break;
        }
        if (dict->next[i] == NO_NEXT)
            printf(" | null\n");
        else
            printf(" | %d\n", dict->next[i]);
    }
    printf("\n");
error:
    return;
}

Dict Dict_new() {
    Dict dict = (Dict)malloc(sizeof(Dict));
    check_mem(dict);

    dict->keys = (DictKey *)malloc(sizeof(DictKey) * DICTSIZE);
    check_mem(dict->keys);
    dict->types = (DictType *)malloc(sizeof(DictType) * DICTSIZE);
    check_mem(dict->types);
    dict->vals = (DictVal *)malloc(sizeof(DictVal) * DICTSIZE);
    check_mem(dict->vals);
    dict->next = (int *)malloc(sizeof(int) * DICTSIZE);
    check_mem(dict->next);

    for (int i = 0; i < DICTSIZE; i++) {
        dict->keys[i] = NULL;
        dict->types[i] = 0;
        dict->vals[i] = (DictVal){._obj_ = NULL};
        dict->next[i] = NO_NEXT;
    }

    return dict;
error:
    return NULL;
}

Dict Dict_delete(Dict dict) {
    if (dict) {
        if (dict->keys)
            free(dict->keys);
        if (dict->types)
            free(dict->types);
        if (dict->vals)
            free(dict->vals);
        if (dict->next)
            free(dict->next);
        free(dict);
    }
    return NULL;
}

int test_dict() {
    log_info("compile successful");
    // DictKey dkeys[DICTSIZE] = {0};
    // DictType dtypes[DICTSIZE] = {0};
    // DictVal dvals[DICTSIZE] = {0};
    // int dnext[DICTSIZE] = {0};
    // for (int i = 0; i < DICTSIZE; i++)
    //     dnext[i] = NO_NEXT;
    // struct DictData ddict =
    //     (struct DictData) {
    //         .keys = &dkeys[0],
    //         .types = &dtypes[0],
    //         .vals = &dvals[0],
    //         .next = &dnext[0]
    // };
    // Dict dict = &ddict;
    Dict dict = Dict_new();
    Dict_set(dict, (DictKey) "pickle", INT, (DictVal){._int_ = 25});
    Dict_set(dict, (DictKey) "cheese", STR, (DictVal){._str_ = "23"});
    Dict_set(dict, (DictKey) "crackers", STR,
             (DictVal){._str_ = "holy guacamole"});
    Dict_set(dict, (DictKey) "crackers2", STR,
             (DictVal){._str_ = "holy guacamole"});
    Dict_printrepr(dict);
    Dict_delkey(dict, (DictKey) "pickle");
    Dict_printrepr(dict);
    Dict_set(dict, (DictKey) "pickle", INT, (DictVal){._int_ = 26});
    Dict_set(dict, (DictKey) "cheese", STR, (DictVal){._str_ = "24"});
    Dict_printrepr(dict);
    Dict_delkey(dict, (DictKey) "pickl");
    debug("getting value of pickle as %d",
          Dict_get(dict, "pickle", EMPTYVAL)._int_);
    Dict_set(dict, (DictKey) "cheese", OBJ, (DictVal){._obj_ = dict});
    Dict_printrepr(dict);
    Dict_delkey(dict, (DictKey) "pickle");
    Dict_delkey(dict, (DictKey) "cheese");
    Dict_delkey(dict, (DictKey) "crackers");
    Dict_printrepr(dict);
    Dict_delete(dict);
    return 0;
}
#endif
#ifdef __DICT_MAIN__
int main(){return 0;}
#endif