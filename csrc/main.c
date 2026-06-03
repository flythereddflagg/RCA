#include "raylib.h"
#include "dbg.h"

#define INIT_PATH "./assets/init.yaml"
#define ASPECT_RATIO (16.0 / 9.0)
#define RESOLUTION 360
#define MAX_SPRITES 256

typedef struct {
    Texture2D image;
    Vector2 position;
} Sprite;

typedef struct {
    unsigned char len;
    Sprite *arr;
} SpriteArray;

void add_sprite(SpriteArray *sprites, Sprite sprite){
    if (sprites->len >= MAX_SPRITES)
        return;
    sprites->arr[sprites->len] = sprite;
    sprites->len += 1;
}

int main(void) {
    InitWindow((int)(RESOLUTION * ASPECT_RATIO), RESOLUTION,
               "Raylib - Red Castle Avenger");
    SetTargetFPS(90);
    Sprite mem[MAX_SPRITES];
    SpriteArray sprites = 
        (SpriteArray)
        {
            .len=0,
            .arr=&(mem[0])
    };
    debug("sizeof everything texture %d image %d", sizeof(Vector2), sizeof(Image));
    add_sprite(&sprites, (Sprite){
        .image=LoadTexture(
            "./assets/scene/red_castle_valley/red_castle_valley_bg.png"),
        .position=(Vector2){0, 0}
    });
    add_sprite(&sprites, (Sprite){
        .image=LoadTexture("assets/actor/larry/larry_base.png"),
        .position=(Vector2){300, 300}   
    });

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(BLACK);
        for (int i = 0; i < sprites.len; i++)
            DrawTexture(
                sprites.arr[i].image, 
                sprites.arr[i].position.x, 
                sprites.arr[i].position.y, 
                WHITE
            );
        EndDrawing();
    }

    for (int i = 0; i < sprites.len; i++)
        UnloadTexture(sprites.arr[i].image);
    CloseWindow();

    return 0;
}
