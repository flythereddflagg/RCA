#include <math.h>
#include <string.h>
#include "dbg.h"
#define DICTKEYLENGTH 256
#define DICTSIZE 3
#define HASHPRIME 31
#define NO_NEXT -1

typedef struct DictData* Dict;
typedef union DictValData DictVal;
typedef char* DictKey;
typedef enum {NONE, DICT, ARR, STR, INT, FLOAT, BOOL} DictType;

union DictValData {
    Dict dict;
    DictVal *arr;
    char *str;
    long long num;
    double fnum;
    unsigned char _bool;
    //NULL none;
};


struct DictData {
    DictKey *keys;
    DictType *types;
    DictVal *vals;
    int *next;
};

int Dict_hash(const DictKey key){
    long long hash = 0; int i = 0;
    for (i = 0; i < DICTKEYLENGTH; i++){
      if (key[i] == '\0') break;
      hash += pow(key[i], i + 1) * HASHPRIME;
    }
    check(i > 0, "invalid hash key");
    debug("hash %lld", hash);
    return hash % DICTSIZE;
    
error:
    return -1;
}

int Dict_set(Dict self, DictKey key, DictType type, DictVal val){
    check(self, "invalid dict supplied");
    check(key[0], "invalid key supplied");
    // get the hash value
    int hash_i = Dict_hash(key), index = 0, i;

    // if the key at that index is not empty follow the linked list to the end
    while (self->next[hash_i] != NO_NEXT)
        hash_i = self->next[hash_i];
    
    index = hash_i;
    // now we have the end of the current hash list
    // so we increment by 1 until we either find an empty slot or the given key
    for (i = 0; i < DICTSIZE; i++){
        if (!self->keys[index] 
            || !strncmp(key, self->keys[index], DICTKEYLENGTH)
        ) break;
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

int Dict_delete(Dict self, DictKey key){
error:
    return -1;
}    

DictVal Dict_get(Dict self, DictKey key, DictVal _default){
    return (DictVal) {.num=0};
}


void Dict_printrepr(Dict dict){
    char *str = "";
    
    for (int i = 0; i < DICTSIZE; i++){
        if (!dict->keys[i]) continue;
        printf("[%3d] %10s | ", i, dict->keys[i]);
        switch (dict->types[i]){
        case NONE:
            printf(" none %20s", "null");
            break;
        case DICT:
        case ARR:
        case STR:
            printf("  str %20s", dict->vals[i].str);
            break;
        case INT:
            printf("  int %20lld", dict->vals[i].num);
            break;
        case FLOAT:
            printf("float %20f", dict->vals[i].fnum);
            break;
        case BOOL:
            printf(" bool %20d", dict->vals[i]._bool);
            break;
        default:
            sentinel("invalid type")
            break;
        }
        if (dict->next[i] == NO_NEXT)
            printf(" | null\n");
        else
            printf(" | %d\n",dict->next[i]);
    }
error:
    return;
}

int main() {
    log_info("compile successful");
    DictKey dkeys[DICTSIZE] = {0};
    DictType dtypes[DICTSIZE] = {0};
    DictVal dvals[DICTSIZE] = {0};
    int dnext[DICTSIZE] = {0};
    for (int i = 0; i < DICTSIZE; i++)
        dnext[i] = NO_NEXT;
    struct DictData ddict = 
        (struct DictData) {
            .keys = &dkeys[0],
            .types = &dtypes[0],
            .vals = &dvals[0],
            .next = &dnext[0]
    };
    Dict dict = &ddict;
    Dict_set(dict, (DictKey)"pickle", INT, (DictVal){.num=25});
    Dict_set(dict, (DictKey)"cheese", STR, (DictVal){.str="23"});
    Dict_set(dict, (DictKey)"crackers", STR, (DictVal){.str="holy guacamole"});

    Dict_printrepr(dict);
    return 0;
}