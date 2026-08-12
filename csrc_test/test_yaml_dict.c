#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <yaml.h>

#include "dbg.h"
#include "dictarr.c"
#define MAX_NESTING_DEPTH 10

typedef enum { YAML_NO_STATE, YAML_MAP_STATE, YAML_SEQ_STATE } yaml_state_t;

DynValue process_yaml_file(const char *filename) {
    DynValue cur_obj = EMPTYVAL;
    int top = -1;
    DictKey cur_key = "";
    DynValue stack[MAX_NESTING_DEPTH] = {EMPTYVAL};
    yaml_state_t levels[MAX_NESTING_DEPTH] = {YAML_NO_STATE};
    FILE *fh = fopen(filename, "rb");
    yaml_parser_t parser;
    yaml_event_t event;
    check(yaml_parser_initialize(&parser),
          "Failed to initialize YAML parser!\n");
    check(fh, "Failed to open file!\n");

    yaml_parser_set_input_file(&parser, fh);

    bool key = false;
    while (yaml_parser_parse(&parser, &event)) {
        switch (event.type) {
        case YAML_MAPPING_START_EVENT:
            cur_obj._dict_ = Dict_new();
            if (top >= 0 && levels[top] == YAML_MAP_STATE) {
                Dict_set(stack[top]._dict_, cur_key, DICT, cur_obj);
            } else if (top >= 0 && levels[top] == YAML_SEQ_STATE) {
                ValArray_append(stack[top]._arr_, DICT, cur_obj);
            }
            top += 1;
            levels[top] = YAML_MAP_STATE;
            stack[top] = cur_obj;
            key = true;
            break;
        case YAML_MAPPING_END_EVENT:
            stack[top] = EMPTYVAL;
            levels[top] = YAML_NO_STATE;
            top -= 1;
            break;
        case YAML_SEQUENCE_START_EVENT:
            cur_obj._arr_ = ValArray_new();
            if (top >= 0 && levels[top] == YAML_MAP_STATE) {
                Dict_set(stack[top]._dict_, cur_key, ARR, cur_obj);
            } else if (top >= 0 && levels[top] == YAML_SEQ_STATE) {
                ValArray_append(stack[top]._arr_, ARR, cur_obj);
            }
            top += 1;
            levels[top] = YAML_SEQ_STATE;
            stack[top] = cur_obj;
            break;
        case YAML_SEQUENCE_END_EVENT:
            stack[top] = EMPTYVAL;
            levels[top] = YAML_NO_STATE;
            top -= 1;
            break;
        case YAML_SCALAR_EVENT:
            if (levels[top] == YAML_SEQ_STATE) {
                printf("- %s\n", event.data.scalar.value);
                ValArray_append(stack[top]._arr_, STR,
                                dynval(_str_, event.data.scalar.value));
            } else if (levels[top] == YAML_MAP_STATE && key) {
                printf("%s : ", event.data.scalar.value);
                cur_key = event.data.scalar.value;
                key = !key;
            } else {
                printf("%s\n", event.data.scalar.value);
                Dict_set(stack[top]._dict_, cur_key, STR,
                         dynval(_str_, event.data.scalar.value));
                key = !key;
            }
            break;
        default:
            break;
        }
        if (event.type == YAML_STREAM_END_EVENT)
            break;

        yaml_event_delete(&event);
    }
error:
    yaml_parser_delete(&parser);
    fclose(fh);
    return stack[0];
}

int main() {
    process_yaml_file("./assets/init.yaml");
    return 0;
}
