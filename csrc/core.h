#ifndef _CORE_H_
#define _CORE_H_
#include "dbg.h"
#include <stdbool.h>
#define EMPTYVAL                                                               \
    (DynValue) { ._obj_ = NULL }
#define dynval(T, V)                                                           \
    (DynValue) { .T = V }
typedef struct DictData *Dict;
typedef union DynValueData DynValue;
typedef enum DynTypeData DynType;
typedef struct ValArrayData *ValArray;
typedef struct GameData *Game;
typedef struct SceneData *Scene;
typedef enum { UP, RIGHT, DOWN, LEFT } Compass;
typedef struct DecalData *Decal;
typedef struct LstringData Lstring;
struct LstringData {
    size_t length;
    char *cstring;
};
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
void Dict_print(Dict dict);
Dict Dict_delete(Dict dict);
void ValArray_print(ValArray arr);
ValArray ValArray_delete(ValArray arr);
#endif
