#include "cyaml.h"
#include "dbg.h"
#include "node.c"
#include "raylib.h"
#include "tools.c"
#include <stdbool.h>

#define INIT_PATH "./assets/init.yaml"
#define ASPECT_RATIO (16.0 / 9.0)
#define RESOLUTION 360
#define MAX_INPUTS 6
#define SPEED 200

typedef enum { NONE, UP, RIGHT, DOWN, LEFT } Direction;

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

void logic(Direction *inputs, NodeArray *nodes) {
    Node larry = nodes->arr[1];
    double dist = SPEED * GetFrameTime();
    for (int i = 0; i < MAX_INPUTS; i++) {
        switch (inputs[i]) {
        case UP:
            larry->decal->position.y -= dist;
            break;

        case DOWN:
            larry->decal->position.y += dist;
            break;

        case RIGHT:
            larry->decal->position.x += dist;
            break;

        case LEFT:
            larry->decal->position.x -= dist;
            break;

        default:
            break;
        }
        inputs[i] = 0;
    }
}

void draw(NodeArray *nodes) {
    BeginDrawing();
    ClearBackground(BLACK);
    for (int i = 0; i < nodes->len; i++)
        DrawTexture(nodes->arr[i]->decal->image,
                    nodes->arr[i]->decal->position.x,
                    nodes->arr[i]->decal->position.y, WHITE);
    EndDrawing();
}

int main(void) {
    // init
    Yaml settings = load_yaml(INIT_PATH);
    InitWindow((int)(RESOLUTION * ASPECT_RATIO), RESOLUTION,
               "Raylib - Red Castle Avenger");
    SetTargetFPS(90);

    Direction input_array[MAX_INPUTS] = {0};
    Direction *inputs = &(input_array[0]);
    SetExitKey(KEY_BACKSPACE);

    Node mem[MAX_NODES];
    NodeArray nodes = (NodeArray){.len = 0, .arr = &(mem[0])};

    NodeArray_add_node(
        &nodes, Node_new(Decal_new(
                    "./assets/scene/red_castle_valley/red_castle_valley_bg.png",
                    (Vector2){0, 0})));
    NodeArray_add_node(&nodes,
                       Node_new(Decal_new("./assets/actor/larry/larry_base.png",
                                          (Vector2){300, 300})));

    // mainloop
    bool running = true;
    while (running) {
        if (WindowShouldClose())
            running = false;
        input(inputs);
        logic(inputs, &nodes);
        draw(&nodes);
    }

    // cleanup
    for (int i = 0; i < nodes.len; i++)
        nodes.arr[i]->delete (nodes.arr[i]);
    cyaml_free(settings);
    CloseWindow();

    return 0;
}
