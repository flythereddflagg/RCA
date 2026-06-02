#include "raylib.h"

#define INIT_PATH "./assets/init.yaml"
#define ASPECT_RATIO (16.0 / 9.0)
#define RESOLUTION 360

int main(void) {
    InitWindow((int)RESOLUTION * ASPECT_RATIO, RESOLUTION,
               "Raylib - Red Castle Avenger");
    SetTargetFPS(90);
    Texture2D background = LoadTexture(
        "./assets/scene/red_castle_valley/red_castle_valley_bg.png");
    Texture2D larry = LoadTexture("assets/actor/larry/larry_base.png");

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(BLACK);
        DrawTexture(background, 0, 0, WHITE);
        DrawTexture(larry, 300, 300, WHITE);
        EndDrawing();
    }
    UnloadTexture(background);
    UnloadTexture(larry);
    CloseWindow();

    return 0;
}
