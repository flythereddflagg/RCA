#ifndef __INPUT_C__
#define __INPUT_C__
#include "dbg.h"
#include "raylib.h"
#include "yaml.c"
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#define MAX_INPUTS 6
#define MAX_CONTROLLERS 4
// #define ACTION_NAME_LEN 8

typedef struct {
    // char name[ACTION_NAME_LEN];
    int id;
    double val;
} Action;

typedef enum {
    UP = KEY_UP,
    DOWN = KEY_DOWN,
    LEFT = KEY_LEFT,
    RIGHT = KEY_RIGHT,
    BUTTON_S = KEY_V,
    BUTTON_E = KEY_SPACE,
    BUTTON_W = KEY_C,
    BUTTON_N = KEY_X,
    START = KEY_ENTER,
    SELECT = KEY_P
} Action_name;

typedef struct InputData *Input;

struct InputData {
    void *parent;
    void *key_bind;
    bool log_input;
    void (*update)(Input self);
    Input (*delete)(Input self);
    Action actions[MAX_INPUTS];
    Action held[MAX_INPUTS];
    Action last_actions[MAX_INPUTS];
    Action new_actions[MAX_INPUTS];
    void *controllers[MAX_CONTROLLERS];
    void *input_log;
};

void Input_hot_plug_check(Input self) { ; }

bool Input_in_last_actions(Input self, Action a) {
    for (int i = 0; i < MAX_INPUTS; i++)
        if (self->last_actions[i].id == a.id)
            return true;
    return false;
}

bool Input_in_held(Input self, Action a) {
    for (int i = 0; i < MAX_INPUTS; i++)
        if (self->held[i].id == a.id)
            return true;
    return false;
}

void Input_update(Input self) {
    Input_hot_plug_check(self);
    // TODO -3- add more player controls player one only for now
    // int player_number = 0;
    int key1 = 0;
    // TODO need to figure out controller input. rn only keyboard
    for (int i = 0; i < MAX_INPUTS; i++) {
        key1 = GetKeyPressed();
        self->actions[i] = (Action){.id = key1, .val = key1 ? 1.0f : 0.0f};
    }
    // update held
    for (int i = 0; i < MAX_INPUTS; i++)
        if (Input_in_last_actions(self, self->actions[i]))
            self->held[i] = self->actions[i];
        else
            self->held[i] = (Action){.id = KEY_NULL, .val = 0.0f};
    // update last actions
    for (int i = 0; i < MAX_INPUTS; i++)
        self->last_actions[i] = self->actions[i];
    // update new actions
    for (int i = 0; i < MAX_INPUTS; i++)
        if (Input_in_held(self, self->actions[i]))
            self->new_actions[i] = (Action){.id = KEY_NULL, .val = 0.0f};
        else
            self->new_actions[i] = self->actions[i];
}

Input Input_delete(Input self) {
    check(self, "'self' is NULL");
    free(self);
error:
    return NULL;
}

void Input_clear(Input self) {
    memset(self->actions, 0, sizeof(self->actions));
    memset(self->held, 0, sizeof(self->held));
    memset(self->last_actions, 0, sizeof(self->last_actions));
    memset(self->new_actions, 0, sizeof(self->new_actions));
}

Input Input_new(void *parent) {
    Input self = (Input)malloc(sizeof(struct InputData));
    check_mem(self);
    self->update = &Input_update;
    self->delete = &Input_delete;
    memset(self->controllers, 0, sizeof(self->controllers));
    Input_clear(self);

error:
    return self;
}

#endif
#ifdef TEST_MAIN
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
