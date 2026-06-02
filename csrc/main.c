#include "raylib.h"

#define INIT_PATH "./assets/init.yaml"
#define ASPECT_RATIO (16.0 / 9.0)
#define RESOLUTION 360

typedef struct {
    Texture2D image;
    Vector2 position;
} Sprite;

int main(void) {
    InitWindow((int)RESOLUTION * ASPECT_RATIO, RESOLUTION,
               "Raylib - Red Castle Avenger");
    SetTargetFPS(90);
    Sprite background = (Sprite){
        .image=LoadTexture(
            "./assets/scene/red_castle_valley/red_castle_valley_bg.png"),
        .position=(Vector2){0, 0}
    };
    Sprite larry = (Sprite){
        .image=LoadTexture("assets/actor/larry/larry_base.png"),
        .position=(Vector2){300, 300}   
    };

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(BLACK);
        DrawTexture(background.image, background.position.x, background.position.y, WHITE);
        DrawTexture(larry.image, larry.position.x, larry.position.y, WHITE);
        EndDrawing();
    }
    UnloadTexture(background.image);
    UnloadTexture(larry.image);
    CloseWindow();

    return 0;
}
