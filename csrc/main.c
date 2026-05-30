#include "raylib.h"

int main(void)
{
    InitWindow(800, 450, "raylib [core] example - basic window");
    SetTargetFPS(90);

    while (!WindowShouldClose())
    {
        BeginDrawing();
            ClearBackground(RAYWHITE);
            DrawText("Congrats! You created your first window!", 190, 200, 20, LIGHTGRAY);
        EndDrawing();
    }

    CloseWindow();

    return 0;
}
