#ifdef __BITMASK_MAIN__
#include "bitmask.h" 
#include <stdio.h>

int main() {
    Image img = LoadImage("./assets/actor/larry/larry_base.png");
    // int width = img.width, height = img.height;
    int width = 32, height = 32;

    BitMask mask = BitMask_from_image(img, DEFAULT_THRESHOLD);
    BitMask_print(mask);
    UnloadImage(img);

    img = BitMask_to_image(mask, WHITE, BLANK);
    mask = BitMask_delete(mask);
    printf("\n");

    mask = BitMask_from_image(img, DEFAULT_THRESHOLD);
    BitMask_print(mask);
    mask = BitMask_delete(mask);
    printf("\n");

    mask = BitMask_new(width, height);
    BitMask_print(mask);
    printf("\n");

    for (int j = 0; j < height; j++) {
        for (int i = 0; i < width; i++) {
            if ((i % 2 == 1 && j % 2 == 1) || (i % 2 == 0 && j % 2 == 0))
                BitMask_set(mask, i, j, true);
        }
    }
    BitMask_print(mask);
    mask = BitMask_delete(mask);
    UnloadImage(img);
    return 0;
}
#endif
#ifdef __COMPASS_MAIN__
int main() { return 0; }
#endif
#ifdef __DICT_MAIN__
#include "dict.h"
int test_dict() {
    log_info("compile successful");
    Dict dict = Dict_new();
    Dict_set(dict, "pickle", INT, dynval(_int_, 25));
    Dict_set(dict, "cheese", STR, dynval(_str_, Lstring_new("23")));
    Dict_set(dict, "crackers", STR,
             dynval(_str_, Lstring_new("holy guacamole")));
    Dict_set(dict, "crackers2", STR,
             dynval(_str_, Lstring_new("holy guacamole")));
    Dict_print(dict);
    Dict_delkey(dict, "pickle");
    Dict_print(dict);
    Dict_set(dict, "pickle", FLOAT, dynval(_float_, 26.2));
    Dict_print(dict);
    Dict_delkey(dict, "pickl");
    debug("getting value of pickle as %f",
          Dict_get(dict, "pickle", EMPTYVAL)._float_);
    Dict_set(dict, "cheese", OBJ, dynval(_obj_, dict));
    Dict_print(dict);
    Dict_delkey(dict, "pickle");
    Dict_delkey(dict, "cheese");
    Dict_delkey(dict, "crackers");
    Dict_print(dict);
    dict = Dict_delete(dict);
    return 0;
}

int main() {
    log_info("compile successful");
    test_dict();
    return 0;
}
#endif
#ifdef __ENGINE_MAIN__
#include "engine.h"
int main() { return 0; }
#endif
#ifdef __INPUT_MAIN__
#include "input.h"
// NOTE: Gamepad name ID depends on drivers and OS
#define XBOX_ALIAS_1 "xbox"
#define XBOX_ALIAS_2 "x-box"
#define PS_ALIAS_1 "playstation"
#define PS_ALIAS_2 "sony"
int main() { return 0; }
int raylib_main(void) {

    const int screenWidth = 800;
    const int screenHeight = 450;

    SetConfigFlags(
        FLAG_MSAA_4X_HINT); // Set MSAA 4X hint before windows creation

    InitWindow(screenWidth, screenHeight,
               "raylib [core] example - input gamepad");

    Texture2D texPs3Pad = LoadTexture("resources/ps3.png");
    Texture2D texXboxPad = LoadTexture("resources/xbox.png");

    // Set axis deadzones
    const float leftStickDeadzoneX = 0.1f;
    const float leftStickDeadzoneY = 0.1f;
    const float rightStickDeadzoneX = 0.1f;
    const float rightStickDeadzoneY = 0.1f;
    const float leftTriggerDeadzone = -0.9f;
    const float rightTriggerDeadzone = -0.9f;

    Rectangle vibrateButton = {0};

    SetTargetFPS(60); // Set our game to run at 60 frames-per-second

    int gamepad = 0; // which gamepad to display
    // TODO look into this. Controller does not seem to be recognized by raylib
    for (int i = 0; i < 100; i++) {
        if (IsGamepadAvailable(i))
            log_info("GP %d: %s", i, GetGamepadName(i));
    }

    // Main game loop
    while (!WindowShouldClose()) // Detect window close button or ESC key
    {
        // Update
        if (IsKeyPressed(KEY_LEFT) && gamepad > 0)
            gamepad--;
        if (IsKeyPressed(KEY_RIGHT))
            gamepad++;
        Vector2 mousePosition = GetMousePosition();

        vibrateButton = (Rectangle){
            10, 70.0f + 20 * GetGamepadAxisCount(gamepad) + 20, 75, 24};
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) &&
            CheckCollisionPointRec(mousePosition, vibrateButton))
            SetGamepadVibration(gamepad, 1.0, 1.0, 1.0);

        // Draw
        BeginDrawing();

        ClearBackground(RAYWHITE);

        if (IsGamepadAvailable(gamepad)) {
            DrawText(TextFormat("GP%d: %s", gamepad, GetGamepadName(gamepad)),
                     10, 10, 10, BLACK);

            // Get axis values
            float leftStickX =
                GetGamepadAxisMovement(gamepad, GAMEPAD_AXIS_LEFT_X);
            float leftStickY =
                GetGamepadAxisMovement(gamepad, GAMEPAD_AXIS_LEFT_Y);
            float rightStickX =
                GetGamepadAxisMovement(gamepad, GAMEPAD_AXIS_RIGHT_X);
            float rightStickY =
                GetGamepadAxisMovement(gamepad, GAMEPAD_AXIS_RIGHT_Y);
            float leftTrigger =
                GetGamepadAxisMovement(gamepad, GAMEPAD_AXIS_LEFT_TRIGGER);
            float rightTrigger =
                GetGamepadAxisMovement(gamepad, GAMEPAD_AXIS_RIGHT_TRIGGER);

            // Calculate deadzones
            if (leftStickX > -leftStickDeadzoneX &&
                leftStickX < leftStickDeadzoneX)
                leftStickX = 0.0f;
            if (leftStickY > -leftStickDeadzoneY &&
                leftStickY < leftStickDeadzoneY)
                leftStickY = 0.0f;
            if (rightStickX > -rightStickDeadzoneX &&
                rightStickX < rightStickDeadzoneX)
                rightStickX = 0.0f;
            if (rightStickY > -rightStickDeadzoneY &&
                rightStickY < rightStickDeadzoneY)
                rightStickY = 0.0f;
            if (leftTrigger < leftTriggerDeadzone)
                leftTrigger = -1.0f;
            if (rightTrigger < rightTriggerDeadzone)
                rightTrigger = -1.0f;

            if ((TextFindIndex(TextToLower(GetGamepadName(gamepad)),
                               XBOX_ALIAS_1) > -1) ||
                (TextFindIndex(TextToLower(GetGamepadName(gamepad)),
                               XBOX_ALIAS_2) > -1)) {
                DrawTexture(texXboxPad, 0, 0, DARKGRAY);

                // Draw buttons: xbox home
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_MIDDLE))
                    DrawCircle(394, 89, 19, RED);

                // Draw buttons: basic
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_MIDDLE_RIGHT))
                    DrawCircle(436, 150, 9, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_MIDDLE_LEFT))
                    DrawCircle(352, 150, 9, RED);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_FACE_LEFT))
                    DrawCircle(501, 151, 15, BLUE);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_FACE_DOWN))
                    DrawCircle(536, 187, 15, LIME);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_FACE_RIGHT))
                    DrawCircle(572, 151, 15, MAROON);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_RIGHT_FACE_UP))
                    DrawCircle(536, 115, 15, GOLD);

                // Draw buttons: d-pad
                DrawRectangle(317, 202, 19, 71, BLACK);
                DrawRectangle(293, 228, 69, 19, BLACK);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_FACE_UP))
                    DrawRectangle(317, 202, 19, 26, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_FACE_DOWN))
                    DrawRectangle(317, 202 + 45, 19, 26, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_FACE_LEFT))
                    DrawRectangle(292, 228, 25, 19, RED);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_LEFT_FACE_RIGHT))
                    DrawRectangle(292 + 44, 228, 26, 19, RED);

                // Draw buttons: left-right back
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_TRIGGER_1))
                    DrawCircle(259, 61, 20, RED);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_TRIGGER_1))
                    DrawCircle(536, 61, 20, RED);

                // Draw axis: left joystick
                Color leftGamepadColor = BLACK;
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_THUMB))
                    leftGamepadColor = RED;
                DrawCircle(259, 152, 39, BLACK);
                DrawCircle(259, 152, 34, LIGHTGRAY);
                DrawCircle(259 + (int)(leftStickX * 20),
                           152 + (int)(leftStickY * 20), 25, leftGamepadColor);

                // Draw axis: right joystick
                Color rightGamepadColor = BLACK;
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_RIGHT_THUMB))
                    rightGamepadColor = RED;
                DrawCircle(461, 237, 38, BLACK);
                DrawCircle(461, 237, 33, LIGHTGRAY);
                DrawCircle(461 + (int)(rightStickX * 20),
                           237 + (int)(rightStickY * 20), 25,
                           rightGamepadColor);

                // Draw axis: left-right triggers
                DrawRectangle(170, 30, 15, 70, GRAY);
                DrawRectangle(604, 30, 15, 70, GRAY);
                DrawRectangle(170, 30, 15, (int)(((1 + leftTrigger) / 2) * 70),
                              RED);
                DrawRectangle(604, 30, 15, (int)(((1 + rightTrigger) / 2) * 70),
                              RED);

                // DrawText(TextFormat("Xbox axis LT: %02.02f",
                // GetGamepadAxisMovement(gamepad, GAMEPAD_AXIS_LEFT_TRIGGER)),
                // 10, 40, 10, BLACK); DrawText(TextFormat("Xbox axis RT:
                // %02.02f", GetGamepadAxisMovement(gamepad,
                // GAMEPAD_AXIS_RIGHT_TRIGGER)), 10, 60, 10, BLACK);
            } else if ((TextFindIndex(TextToLower(GetGamepadName(gamepad)),
                                      PS_ALIAS_1) > -1) ||
                       (TextFindIndex(TextToLower(GetGamepadName(gamepad)),
                                      PS_ALIAS_2) > -1)) {
                DrawTexture(texPs3Pad, 0, 0, DARKGRAY);

                // Draw buttons: ps
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_MIDDLE))
                    DrawCircle(396, 222, 13, RED);

                // Draw buttons: basic
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_MIDDLE_LEFT))
                    DrawRectangle(328, 170, 32, 13, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_MIDDLE_RIGHT))
                    DrawTriangle((Vector2){436, 168}, (Vector2){436, 185},
                                 (Vector2){464, 177}, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_RIGHT_FACE_UP))
                    DrawCircle(557, 144, 13, LIME);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_FACE_RIGHT))
                    DrawCircle(586, 173, 13, RED);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_FACE_DOWN))
                    DrawCircle(557, 203, 13, VIOLET);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_FACE_LEFT))
                    DrawCircle(527, 173, 13, PINK);

                // Draw buttons: d-pad
                DrawRectangle(225, 132, 24, 84, BLACK);
                DrawRectangle(195, 161, 84, 25, BLACK);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_FACE_UP))
                    DrawRectangle(225, 132, 24, 29, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_FACE_DOWN))
                    DrawRectangle(225, 132 + 54, 24, 30, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_FACE_LEFT))
                    DrawRectangle(195, 161, 30, 25, RED);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_LEFT_FACE_RIGHT))
                    DrawRectangle(195 + 54, 161, 30, 25, RED);

                // Draw buttons: left-right back buttons
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_TRIGGER_1))
                    DrawCircle(239, 82, 20, RED);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_TRIGGER_1))
                    DrawCircle(557, 82, 20, RED);

                // Draw axis: left joystick
                Color leftGamepadColor = BLACK;
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_THUMB))
                    leftGamepadColor = RED;
                DrawCircle(319, 255, 35, BLACK);
                DrawCircle(319, 255, 31, LIGHTGRAY);
                DrawCircle(319 + (int)(leftStickX * 20),
                           255 + (int)(leftStickY * 20), 25, leftGamepadColor);

                // Draw axis: right joystick
                Color rightGamepadColor = BLACK;
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_RIGHT_THUMB))
                    rightGamepadColor = RED;
                DrawCircle(475, 255, 35, BLACK);
                DrawCircle(475, 255, 31, LIGHTGRAY);
                DrawCircle(475 + (int)(rightStickX * 20),
                           255 + (int)(rightStickY * 20), 25,
                           rightGamepadColor);

                // Draw axis: left-right triggers
                DrawRectangle(169, 48, 15, 70, GRAY);
                DrawRectangle(611, 48, 15, 70, GRAY);
                DrawRectangle(169, 48, 15, (int)(((1 + leftTrigger) / 2) * 70),
                              RED);
                DrawRectangle(611, 48, 15, (int)(((1 + rightTrigger) / 2) * 70),
                              RED);
            } else {
                // Draw background: generic
                DrawRectangleRounded((Rectangle){175, 110, 460, 220}, 0.3f, 16,
                                     DARKGRAY);

                // Draw buttons: basic
                DrawCircle(365, 170, 12, RAYWHITE);
                DrawCircle(405, 170, 12, RAYWHITE);
                DrawCircle(445, 170, 12, RAYWHITE);
                DrawCircle(516, 191, 17, RAYWHITE);
                DrawCircle(551, 227, 17, RAYWHITE);
                DrawCircle(587, 191, 17, RAYWHITE);
                DrawCircle(551, 155, 17, RAYWHITE);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_MIDDLE_LEFT))
                    DrawCircle(365, 170, 10, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_MIDDLE))
                    DrawCircle(405, 170, 10, GREEN);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_MIDDLE_RIGHT))
                    DrawCircle(445, 170, 10, BLUE);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_FACE_LEFT))
                    DrawCircle(516, 191, 15, GOLD);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_FACE_DOWN))
                    DrawCircle(551, 227, 15, BLUE);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_FACE_RIGHT))
                    DrawCircle(587, 191, 15, GREEN);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_RIGHT_FACE_UP))
                    DrawCircle(551, 155, 15, RED);

                // Draw buttons: d-pad
                DrawRectangle(245, 145, 28, 88, RAYWHITE);
                DrawRectangle(215, 174, 88, 29, RAYWHITE);
                DrawRectangle(247, 147, 24, 84, BLACK);
                DrawRectangle(217, 176, 84, 25, BLACK);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_FACE_UP))
                    DrawRectangle(247, 147, 24, 29, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_FACE_DOWN))
                    DrawRectangle(247, 147 + 54, 24, 30, RED);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_FACE_LEFT))
                    DrawRectangle(217, 176, 30, 25, RED);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_LEFT_FACE_RIGHT))
                    DrawRectangle(217 + 54, 176, 30, 25, RED);

                // Draw buttons: left-right back
                DrawRectangleRounded((Rectangle){215, 98, 100, 10}, 0.5f, 16,
                                     DARKGRAY);
                DrawRectangleRounded((Rectangle){495, 98, 100, 10}, 0.5f, 16,
                                     DARKGRAY);
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_TRIGGER_1))
                    DrawRectangleRounded((Rectangle){215, 98, 100, 10}, 0.5f,
                                         16, RED);
                if (IsGamepadButtonDown(gamepad,
                                        GAMEPAD_BUTTON_RIGHT_TRIGGER_1))
                    DrawRectangleRounded((Rectangle){495, 98, 100, 10}, 0.5f,
                                         16, RED);

                // Draw axis: left joystick
                Color leftGamepadColor = BLACK;
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_LEFT_THUMB))
                    leftGamepadColor = RED;
                DrawCircle(345, 260, 40, BLACK);
                DrawCircle(345, 260, 35, LIGHTGRAY);
                DrawCircle(345 + (int)(leftStickX * 20),
                           260 + (int)(leftStickY * 20), 25, leftGamepadColor);

                // Draw axis: right joystick
                Color rightGamepadColor = BLACK;
                if (IsGamepadButtonDown(gamepad, GAMEPAD_BUTTON_RIGHT_THUMB))
                    rightGamepadColor = RED;
                DrawCircle(465, 260, 40, BLACK);
                DrawCircle(465, 260, 35, LIGHTGRAY);
                DrawCircle(465 + (int)(rightStickX * 20),
                           260 + (int)(rightStickY * 20), 25,
                           rightGamepadColor);

                // Draw axis: left-right triggers
                DrawRectangle(151, 110, 15, 70, GRAY);
                DrawRectangle(644, 110, 15, 70, GRAY);
                DrawRectangle(151, 110, 15, (int)(((1 + leftTrigger) / 2) * 70),
                              RED);
                DrawRectangle(644, 110, 15,
                              (int)(((1 + rightTrigger) / 2) * 70), RED);
            }

            DrawText(
                TextFormat("DETECTED AXIS [%i]:", GetGamepadAxisCount(gamepad)),
                10, 50, 10, MAROON);

            for (int i = 0; i < GetGamepadAxisCount(gamepad); i++) {
                DrawText(TextFormat("AXIS %i: %.02f", i,
                                    GetGamepadAxisMovement(gamepad, i)),
                         20, 70 + 20 * i, 10, DARKGRAY);
            }

            // Draw vibrate button
            DrawRectangleRec(vibrateButton, SKYBLUE);
            DrawText("VIBRATE", (int)(vibrateButton.x + 14),
                     (int)(vibrateButton.y + 1), 10, DARKGRAY);

            if (GetGamepadButtonPressed() != GAMEPAD_BUTTON_UNKNOWN)
                DrawText(TextFormat("DETECTED BUTTON: %i",
                                    GetGamepadButtonPressed()),
                         10, 430, 10, RED);
            else
                DrawText("DETECTED BUTTON: NONE", 10, 430, 10, GRAY);
        } else {
            DrawText(TextFormat("GP%d: NOT DETECTED", gamepad), 10, 10, 10,
                     GRAY);
            DrawTexture(texXboxPad, 0, 0, LIGHTGRAY);
        }

        EndDrawing();
    }

    // De-Initialization
    UnloadTexture(texPs3Pad);
    UnloadTexture(texXboxPad);

    CloseWindow(); // Close window and OpenGL context

    return 0;
}
#endif
#ifdef __LSTRING_MAIN__
#include "lstring.h"
int main() {
    Lstring str = Lstring_new("Its a string!");
    Lstring str2 = Lstring_new("Its a string?");
    log_info("equal? %d", Lstring_equal(str, str2));
    str2.cstring[str2.length - 1] = '!';
    log_info("how bout now? %d", Lstring_equal(str, str2));
    log_info("C string equal? %d", Lstring_cstring_equal("boy", "girl"));

    Lstring_print(str);
    printf("\n");
    str = Lstring_delete(str);
    str2 = Lstring_delete(str2);
    return 0;
}
#endif
#ifdef __NODE_MAIN__
#include "node.h"
#include "yaml_parse.h"
int test_node_from_dict() {
    DynValue out =
        YamlParse_process_yaml_file("./assets/scene/test_scene.yaml");
    Dict scene_init = out._dict_;
    Dict node_init =
        ValArray_get_at(Dict_get(scene_init, "nodes", EMPTYVAL)._arr_, 0)
            ._dict_;
    Node node = Node_from_dict(node_init);
    node = Node_delete(node);
    Dict_delete(scene_init);
    return 0;
}
int main() {
    NodeGroup group = NodeGroup_new();
    NodeGroup group2 = NodeGroup_new();

    Node node = Node_new();
    debug("deleting node");
    node = node->delete (node);
    debug("remaking node");
    node = Node_new();
    Node_add_child(node, Node_new());

    Node_add(node, group);
    NodeGroup_add(group2, node);
    NodeGroup_add(group, (Node)ObjList_at(node->children, 0));
    debug("group->length: %lu", group->length);
    debug("group2->length: %lu", group2->length);
    debug("killing node");
    node = Node_kill(node);
    debug("group->length: %lu", group->length);
    debug("group2->length: %lu", group2->length);
    group = NodeGroup_delete(group);
    group2 = NodeGroup_delete(group2);
    node->delete (node);
    test_node_from_dict();
    return 0;
}
#endif
#ifdef __OBJLIST_MAIN__
#include "objlist.h"
int main() {
    ObjList list = ObjList_new();
    ObjList_push(list, "cheese");
    char *cheese = (char *)ObjList_pop(list);
    debug("%s", cheese);
    ObjList_push(list, "cheese!");
    ObjList_push(list, "crackers");
    ObjList_push(list, "sausage");
    ObjList_push(list, "naan");
    ObjList_push(list, "charcuterie");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list, i));
    }
    debug("\n\n-- getting and setting --\n");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_set_at(list, i, "peas"));
    }
    debug("\n\n-- after setting --\n");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list, i));
    }
    ObjList_insert(list, 0, "cheese! 0");
    ObjList_insert(list, 3, "cheese! 3");
    ObjList_insert(list, 2, "cheese! 2");
    ObjList_insert(list, 0, "cheese! 00");
    ObjList_insert(list, 2, "cheese! 2");
    ObjList_insert(list, list->length, "cheese! end");
    debug("\n\n-- after inserting --\n");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list, i));
    }
    debug("\n\n-- removing --\n");

    debug("at %lu got '%s'", (size_t)2, (char *)ObjList_remove_at(list, 2));
    debug("at %lu got '%s'", (size_t)0, (char *)ObjList_remove_at(list, 0));
    debug("at %lu got '%s'", (size_t)5, (char *)ObjList_remove_at(list, 5));
    debug("at %lu got '%s'", (size_t)3, (char *)ObjList_remove_at(list, 3));
    debug("at %lu got '%s'", (size_t)2, (char *)ObjList_remove_at(list, 2));
    debug("at %lu got '%s'", list->length - 1,
          (char *)ObjList_remove_at(list, list->length - 1));
    debug("\n\n-- after removing --\n");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list, i));
    }
    debug("\n\n-- has? --\n");
    debug("list has '%s'? %s", (char *)ObjList_at(list, 3),
          ObjList_has(list, ObjList_at(list, 3)) ? "true" : "false");
    debug("list has '%s'? %s", "not cheese",
          ObjList_has(list, "not cheese") ? "true" : "false");
    debug("\n\n-- concat --\n");
    ObjList list2 = ObjList_new();
    ObjList_extend(list2, list);
    for (size_t i = 0; i < list2->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list2, i));
    }
    ObjList_delete(list);
    ObjList_delete(list2);
    return 0;
}
#endif
#ifdef __PLAYER_MAIN__
#include "player.h"
int main() { return 0; }
#endif
#ifdef __SCENE_MAIN__
#include "scene.h"
int main() {
    Scene scene = Scene_new(NULL, "./assets/scene/test_scene.yaml", NULL, NULL);
    Scene_setup(scene);
    // Dict_print(scene->init);
    check(!Scene_deconstruct(scene), "deconstruct failed");
    scene = Scene_delete(scene);
    return 0;
error:
    return 23;
}
#endif
#ifdef __SPRITE_MAIN__
#include "sprite.h"
int main() { return 0; }
#endif
#ifdef __VALARRAY_MAIN__
#include "valarray.h"
int test_arr() {
    int len = 10;
    ValArray arr = ValArray_new();
    ValArray_print(arr);
    printf("\n");

    for (int i = 0; i < len; i++) {
        ValArray_append(arr, INT, dynval(_int_, 0));
    }
    ValArray_insert(arr, 3, INT, dynval(_int_, 5));
    ValArray_append(arr, STR, dynval(_str_, Lstring_new("a string")));

    ValArray_print(arr);
    printf("\n");
    debug("%d", ValArray_remove(arr, 3)._int_);
    ValArray_print(arr);
    printf("\n");
    arr = ValArray_delete(arr);
    ValArray_print(arr); // should cause an error.

    return 0;
}
int main() {
    test_arr();
    return 0;
}
#endif
#ifdef __YAML_PARSE_MAIN__
#include "yaml_parse.h"
#include <yaml.h>
int test_dict() {
    Dict out =
        YamlParse_process_yaml_file("./assets/scene/startup.yaml")._dict_;
    out = Dict_delete(out);
    return 0;
}

int test_init() {
    DynValue out = YamlParse_process_yaml_file("./assets/init.yaml");
    Dict dict = out._dict_;
    log_info("FINAL DICT");
    Dict_print(out._dict_);
    printf("\n");
    ValArray aspect_ratio_parts =
        Dict_get(dict, "ASPECT_RATIO", EMPTYVAL)._arr_;
    check(aspect_ratio_parts, "ValArray Failed to load.");
    ValArray_print(aspect_ratio_parts);
    printf("\n");
    Dict_delete(out._dict_);
    return 0;

error:
    Dict_delete(out._dict_);
    return -1;
}
int main() {
    test_dict();
    test_init();
    return 0;
}
#endif
