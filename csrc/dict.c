#include <math.h>
#include <string.h>
#include "dbg.h"
#define DICTKEYLENGTH 256
#define DICTSIZE 255
#define HASHPRIME 31

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
    debug("hash %lld\n", hash);
    return hash % DICTSIZE;
    
error:
    return -1;
}

int Dict_set(Dict self, DictKey key, DictType type, DictVal val){
    int index = Dict_hash(key);
    if ((*self->keys[index]) && strncmp(key, self->keys[index], DICTKEYLENGTH)){
        
    }
    check(index >= 0 && index < DICTSIZE, "invalid index detected");
    self->keys[index] = key;
    self->types[index] = type;
    self->vals[index] = val;
    return 0;
error:
    return -1;
}
    

DictVal Dict_get(Dict self, DictKey key, DictVal _default){
    return (DictVal) {.num=0};
}

void Dict_printrepr(Dict yaml){
    char *str = "";
    
    for (int i = 0; i < DICTSIZE; i++){
        if (!yaml->keys[i]) continue;
        printf("[%3d] %10s | ", i, yaml->keys[i]);
        switch (yaml->types[i]){
        case NONE:
            printf(" none %20s", "NONE");
            break;
        case DICT:
        case ARR:
        case STR:
            printf("  str %20s", yaml->vals[i].str);
            break;
        case INT:
            printf("  int %20lld", yaml->vals[i].num);
            break;
        case FLOAT:
            printf("float %20f", yaml->vals[i].fnum);
            break;
        case BOOL:
            printf(" bool %20d", yaml->vals[i]._bool);
            break;
        default:
            sentinel("invalid type")
            break;
        }
        printf(" | %d\n",yaml->next[i]);
    }
error:
    return;
}

int main() {
    log_info("\n compile successful\n");
    DictKey dkeys[DICTSIZE] = {""};
    DictType dtypes[DICTSIZE] = {NONE};
    DictVal dvals[DICTSIZE] = {0};
    int dnext[DICTSIZE] = {-1};    
    struct DictData dyaml = 
        (struct DictData) {
            .keys = &dkeys[0],
            .types = &dtypes[0],
            .vals = &dvals[0],
            .next = &dnext[0]
    };
    Dict yaml = &dyaml;
    Dict_set(yaml, (DictKey)"pickle", INT, (DictVal){.num=25});
    Dict_set(yaml, (DictKey)"cheese", STR, (DictVal){.str="23"});
    Dict_printrepr(yaml);
    return 0;
}