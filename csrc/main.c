#include "dbg.h"
#include "raylib.h"
#include "node.h"
#include <stdbool.h>

#define INIT_PATH "./assets/init.yaml"
#define ASPECT_RATIO (16.0 / 9.0)
#define RESOLUTION 360
#define MAX_SPRITES 256
#define MAX_INPUTS 6
#define SPEED 200

typedef struct {
    Texture2D image;
    Vector2 position;
} Sprite;

typedef struct {
    unsigned char len;
    Sprite *arr;
} SpriteArray;

typedef enum { NONE, UP, RIGHT, DOWN, LEFT } Direction;

void add_sprite(SpriteArray *sprites, Sprite sprite) {
    if (sprites->len >= MAX_SPRITES)
        return;
    sprites->arr[sprites->len] = sprite;
    sprites->len += 1;
}

void input(Direction *inputs) {
    if (IsKeyDown(KEY_UP))
        inputs[0] = UP;
    if (IsKeyDown(KEY_DOWN))
        inputs[1] = DOWN;
    if (IsKeyDown(KEY_LEFT))
        inputs[2] = LEFT;
    if (IsKeyDown(KEY_RIGHT))
        inputs[3] = RIGHT;
}

void logic(Direction *inputs, SpriteArray *sprites) {
    Sprite *larry = &(sprites->arr[1]);
    double dist = SPEED * GetFrameTime();
    for (int i = 0; i < MAX_INPUTS; i++) {
        switch (inputs[i]) {
        case UP:
            larry->position.y -= dist;
            break;

        case DOWN:
            larry->position.y += dist;
            break;

        case RIGHT:
            larry->position.x += dist;
            break;

        case LEFT:
            larry->position.x -= dist;
            break;

        default:;
        }
        inputs[i] = 0;
    }
}

void draw(SpriteArray *sprites) {
    BeginDrawing();
    ClearBackground(BLACK);
    for (int i = 0; i < sprites->len; i++)
        DrawTexture(sprites->arr[i].image, sprites->arr[i].position.x,
                    sprites->arr[i].position.y, WHITE);
    EndDrawing();
}

int main(void) {
    // init
    InitWindow((int)(RESOLUTION * ASPECT_RATIO), RESOLUTION,
               "Raylib - Red Castle Avenger");
    SetTargetFPS(90);
    Sprite mem[MAX_SPRITES];
    SpriteArray sprites = (SpriteArray){.len = 0, .arr = &(mem[0])};
    add_sprite(&sprites,(Sprite){
        .image = LoadTexture(
                "./assets/scene/red_castle_valley/red_castle_valley_bg.png"
        ),
        .position = (Vector2){0, 0}
    });
    add_sprite(&sprites, (Sprite){
        .image = LoadTexture("assets/actor/larry/larry_base.png"),
        .position = (Vector2){300, 300}
    });
    Direction input_array[MAX_INPUTS] = {0};
    Direction *inputs = &(input_array[0]);
    SetExitKey(KEY_BACKSPACE);

    // mainloop
    bool running = true;
    while (running) {
        if (WindowShouldClose())
            running = false;
        input(inputs);
        logic(inputs, &sprites);
        draw(&sprites);
    }

    // cleanup
    for (int i = 0; i < sprites.len; i++)
        UnloadTexture(sprites.arr[i].image);
    CloseWindow();

    return 0;
}
