#ifndef _CORE_H_
#define _CORE_H_
#include "dbg.h"
#include <stdbool.h>
#define EMPTYVAL                                                               \
    (DynValue) { ._obj_ = NULL }
#define dynval(T, V)                                                           \
    (DynValue) { .T = V }
#define LSTRING_FMT "%.*s"

typedef struct NodeData *Node;
typedef struct DictData *Dict;
typedef union DynValueData DynValue;
typedef enum DynTypeData DynType;
typedef struct ValArrayData *ValArray;
typedef struct GameData *Game;
typedef struct SceneData *Scene;
typedef enum { UP, RIGHT, DOWN, LEFT } Compass;
typedef struct SpriteData *Sprite;
typedef struct LstringData Lstring;

// forward delcar all setup functions
int Node_setup(Node node);
int Backpack_setup(Node node);
int Camera_setup(Node node);
int CutScene_setup(Node node);
int Edge_setup(Node node);
int Item_setup(Node node);
int Music_setup(Node node);
int Retry_setup(Node node);
int SoftDirt_setup(Node node);
int TextRoll_setup(Node node);
int Animation_setup(Node node);
int Cactus_setup(Node node);
int Coin_setup(Node node);
int Decal_setup(Node node);
int Gate_setup(Node node);
int Menu_setup(Node node);
int OpenUrlTrigger_setup(Node node);
int SFX_setup(Node node);
int TextBox_setup(Node node);
int Trigger_setup(Node node);

struct LstringData {
    size_t length;
    char *cstring;
    bool on_heap;
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
