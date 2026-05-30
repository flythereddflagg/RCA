#include "raylib.h"

#define INIT_PATH "./assets/init.yaml"
#define ASPECT_RATIO (16.0 / 9.0)
#define RESOLUTION 360


int main(void)
{
    InitWindow(
        (int) RESOLUTION * ASPECT_RATIO, 
        RESOLUTION, 
        "Raylib - Red Castle Avenger"
    );
    SetTargetFPS(90);
    Image image = LoadImage(
        "./assets/scene/red_castle_valley/red_castle_valley_bg.png"
    );
    Texture2D background = LoadTextureFromImage(image);

    while (!WindowShouldClose())
    {
        BeginDrawing();
            ClearBackground(BLACK);
            DrawTexture(background, 0, 0, WHITE);
        EndDrawing();
    }
    UnloadTexture(background);
    UnloadImage(image);
    CloseWindow();

    return 0;
}
