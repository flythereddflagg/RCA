#ifndef __INPUT_C__
#define __INPUT_C__
#include "dbg.h"
#include "raylib.h"
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#define MAX_INPUTS 6
#define MAX_CONTROLLERS 4

typedef struct InputData *Input;

struct InputData {
    void *parent;
    void *key_bind;
    bool log_input;
    void (*update)(const void *self);
    void (*delete)(Input self);
    char actions[MAX_INPUTS];
    char held[MAX_INPUTS];
    char last_actions[MAX_INPUTS]; 
    void *controllers[MAX_CONTROLLERS];
    void *input_log;
};

void Input_update(const void *self) { ; }

void Input_delete(Input self) {
    check(self, "'self' is NULL");
    free(self);
error:;
}

Input Input_new(void *parent, void *binds) {
    Input self = (Input)malloc(sizeof(struct InputData));
    check_mem(self);
    self->update = &Input_update;
    self->delete = &Input_delete;
    memset(self->actions, 0, sizeof(self->actions));
    memset(self->held, 0, sizeof(self->held));
    memset(self->last_actions, 0, sizeof(self->last_actions));
    memset(self->controllers, 0, sizeof(self->controllers));   

error:
    return self;
}

#endif
