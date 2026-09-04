#ifndef _CORE_H_
#define _CORE_H_
#include "dbg.h"
typedef struct DictData *Dict;
typedef union DynValueData DynValue;
typedef enum DynTypeData DynType;
typedef struct ValArrayData *ValArray;
typedef struct GameData *Game;
typedef struct SceneData *Scene;
typedef enum { UP, RIGHT, DOWN, LEFT } Compass;
typedef struct DecalData *Decal;
typedef struct LstringData Lstring;
#endif