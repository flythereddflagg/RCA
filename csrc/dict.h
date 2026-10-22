#ifndef __DICT_H__
#define __DICT_H__
#include "lstring.h"
#define DICTSIZE 256
#define HASHPRIME 31
#define NO_NEXT -1
#define dynval(T, V)                                                           \
    (DynValue) { .T = V }
#define EMPTYVAL                                                               \
    (DynValue) { ._obj_ = NULL }

typedef struct DictData *Dict;
typedef union DynValueData DynValue;
typedef enum DynTypeData DynType;
typedef struct ValArrayData *ValArray;
void ValArray_print(ValArray arr);
ValArray ValArray_delete(ValArray arr);
enum DynTypeData { NONE, DICT, ARR, STR, INT, FLOAT, BOOL, OBJ };
union DynValueData {
    Dict _dict_;
    ValArray _arr_;
    Lstring _str_;
    int _int_;
    float _float_;
    bool _bool_;
    void *_obj_;
    // NULL none;
};
struct DictData {
    Lstring *keys;
    DynType *types;
    DynValue *vals;
    int *next;
};
void Dict_print(Dict dict);
Dict Dict_delete(Dict dict);
int Dict_hash(const Lstring key);
int Dict_get_index(const Dict dict, const Lstring key);
int Dict_set(Dict dict, char *cstring, DynType type, DynValue val);
int Dict_delkey(Dict dict, char *cstring);
DynValue Dict_get(Dict dict, char *cstring, DynValue _default);
bool Dict_key_in(Dict dict, char *key);
void Dict_print(Dict dict);
void Dict_debug_print(Dict dict);
Dict Dict_new();
Dict Dict_copy(Dict dict);
Dict Dict_delete(Dict dict);
int test_dict();

struct ValArrayData {
    int length;
    DynValue *vals;
    DynType *types;
};
ValArray ValArray_new();
ValArray ValArray_delete(ValArray arr);
DynValue ValArray_get_at(ValArray arr, int index);
DynType ValArray_type_at(ValArray arr, int index);
int ValArray_set_at(ValArray arr, int index, DynType type, DynValue val);
int ValArray_append(ValArray arr, DynType type, DynValue val);
int ValArray_insert(ValArray arr, int index, DynType type, DynValue val);
DynValue ValArray_remove(ValArray arr, int index);
bool ValArray_has_string(ValArray arr, char *cstring);
int ValArray_extend(ValArray arr1, ValArray arr2);
void ValArray_print(ValArray arr);
ValArray ValArray_copy(ValArray arr);
int test_arr();

#endif
