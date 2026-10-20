#ifndef __INPUT_H__
#define __INPUT_H__

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

void Input_hot_plug_check(Input self);
bool Input_in_last_actions(Input self, Action a);
bool Input_in_held(Input self, Action a);
void Input_update(Input self);
Input Input_delete(Input self);
void Input_clear(Input self);
Input Input_new(void *parent);
int raylib_main(void);

#endif
