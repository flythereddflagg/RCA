#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <yaml.h>

#include "dbg.h"
#include "dictarr.c"
#include "lstring.c"
#define MAX_NESTING_DEPTH 10

typedef enum { YAML_NO_STATE, YAML_MAP_STATE, YAML_SEQ_STATE } yaml_state_t;

DynValue process_yaml_file(const char *filename) {
    DynValue cur_obj = EMPTYVAL;
    DynValue out_obj = EMPTYVAL;
    int top = -1;
    Lstring cur_key = Lstring_new("");
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
        if (out_obj._obj_ == NULL && cur_obj._obj_ != NULL)
            out_obj = cur_obj;
        switch (event.type) {
        case YAML_MAPPING_START_EVENT:
            cur_obj._dict_ = Dict_new();
            if (top >= 0 && levels[top] == YAML_MAP_STATE) {
                Dict_set(stack[top]._dict_, cur_key.cstring, DICT, cur_obj);
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
                Dict_set(stack[top]._dict_, cur_key.cstring, ARR, cur_obj);
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
                // printf("- %s\n", event.data.scalar.value);
                ValArray_append(
                    stack[top]._arr_, STR,
                    dynval(_str_,
                           Lstring_new((char *)event.data.scalar.value)));
            } else if (levels[top] == YAML_MAP_STATE && key) {
                // printf("%s : ", event.data.scalar.value);
                cur_key = Lstring_set(cur_key, (char *)event.data.scalar.value);
                key = !key;
            } else {
                // printf("%s\n", event.data.scalar.value);
                Dict_set(stack[top]._dict_, cur_key.cstring, STR,
                         dynval(_str_,
                                Lstring_new((char *)event.data.scalar.value)));
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
    cur_key = Lstring_delete(cur_key);
    return out_obj;
}

int main() {
    DynValue out = process_yaml_file("./assets/init.yaml");
    log_info("FINAL DICT");
    Dict_print(out._dict_);
    Dict_delete(out._dict_);
    return 0;
}
/*
==31402==
==31402== HEAP SUMMARY:
==31402==     in use at exit: 86,667 bytes in 195 blocks
==31402==   total heap usage: 1,000 allocs, 805 frees, 185,162 bytes allocated
==31402==
==31402== LEAK SUMMARY:
==31402==    definitely lost: 12,653 bytes in 26 blocks
==31402==    indirectly lost: 74,014 bytes in 169 blocks
==31402==      possibly lost: 0 bytes in 0 blocks
==31402==    still reachable: 0 bytes in 0 blocks
==31402==         suppressed: 0 bytes in 0 blocks
==31402== Rerun with --leak-check=full to see details of leaked memory
==31402==
==31402== For lists of detected and suppressed errors, rerun with: -s
==31402== ERROR SUMMARY: 25 errors from 12 contexts (suppressed: 0 from 0)
*/
