#ifndef __INPUT_H__
#define __INPUT_H__
#include "dbg.h"
#include "raylib.h"
#include "yaml_parse.h"
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#define MAX_INPUTS 6
#define MAX_CONTROLLERS 4

typedef struct {
    // char name[ACTION_NAME_LEN];
    int id;
    double val;
} Action;
typedef enum {
    BUTTON_UP = KEY_UP,
    BUTTON_DOWN = KEY_DOWN,
    BUTTON_LEFT = KEY_LEFT,
    BUTTON_RIGHT = KEY_RIGHT,
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
    Action actions[MAX_INPUTS];
    Action held[MAX_INPUTS];
    Action last_actions[MAX_INPUTS];
    Action new_actions[MAX_INPUTS];
    void *controllers[MAX_CONTROLLERS];
    void *input_log;
};

void Input_hot_plug_check(Input input);
bool Input_in_last_actions(Input input, Action a);
bool Input_in_held(Input input, Action a);
int Input_update(Input input);
Input Input_delete(Input input);
void Input_clear(Input input);
Input Input_new(void *parent);
int raylib_main(void);

#endif
