#include <stdbool.h>
#include "raylib.h"
#include "dbg.h"

#include "node.c"
#include "tools.c"


#define INIT_PATH "./assets/init.yaml"
#define ASPECT_RATIO (16.0 / 9.0)
#define MAX_INPUTS 6
#define SPEED 200

typedef enum {NO_DIR, UP, RIGHT, DOWN, LEFT } Direction;

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

RenderTexture2D init_screen(Yaml settings){
    RenderTexture2D val;
    int resolution = Yaml_get(settings, "RESOLUTION").num;
    char *title = Yaml_get(settings, "title").str;
    double aspect_ratio = (
        1.0f * Yaml_get(settings, "/ASPECT_RATIO[0]").num
        / Yaml_get(settings, "/ASPECT_RATIO[1]").num
    );
    InitWindow((int)(resolution * aspect_ratio), resolution, title);
    SetTargetFPS(Yaml_get(settings, "FPS").num);
    SetExitKey(KEY_BACKSPACE);
    return val;
}



int main(void) {
    // init
    Node mem[MAX_NODES];
    NodeArray nodes = (NodeArray){.len = 0, .arr = &(mem[0])};
    
    Yaml settings = Yaml_load(INIT_PATH);
    check(settings, "Settings could not load");
    
    // void *scene = NULL;
    // void *saved_scenes = NULL;

    // RenderTexture2D screen = 
    init_screen(settings);

    Direction input_array[MAX_INPUTS] = {0};
    Direction *inputs = &(input_array[0]);

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
    Yaml_delete(settings);
    CloseWindow();
    return 0;

error:
    // cleanup
    for (int i = 0; i < nodes.len; i++)
        nodes.arr[i]->delete(nodes.arr[i]);
    Yaml_delete(settings);
    CloseWindow();
    return 1;
}
