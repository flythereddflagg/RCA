

#include "raylib.h"

Vector2 unit(Compass dir) {
    switch (dir) {
    case UP:
        return (Vector2){0, -1};
        break;
    case RIGHT:
        return (Vector2){1, 0};
        break;
    case DOWN:
        return (Vector2){0, 1};
        break;
    case LEFT:
        return (Vector2){-1, 0};
        break;
    default:
        return (Vector2){0, 0};
        break;
    }
}

#ifdef __COMPASS_MAIN__
int main() { return 0; }
#endif
