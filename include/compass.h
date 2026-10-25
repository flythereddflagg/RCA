#ifndef __COMPASS_H__
#define __COMPASS_H__
#include "raylib.h"
typedef enum { UP, RIGHT, DOWN, LEFT } Compass;
Vector2 unit(Compass dir);

#endif
