#ifndef __COMPASS_H__
#define __COMPASS_H__
typedef enum { UP, RIGHT, DOWN, LEFT } Compass;
Vector2 unit(Compass dir);

#endif
