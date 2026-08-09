#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <yaml.h>

#include "dbg.h"
#include "dictarr.c"
#define MAX_NESTING_DEPTH 10

typedef enum { YAML_NO_STATE, YAML_MAP_STATE, YAML_SEQ_STATE } yaml_state_t;

DynValue process_yaml_file(const char *filename) {
    DynValue output_obj = EMPTYVAL;
    DynValue cur_obj = EMPTYVAL;
    FILE *fh = fopen(filename, "rb");
    yaml_parser_t parser;
    yaml_event_t event;
    check(yaml_parser_initialize(&parser),
          "Failed to initialize YAML parser!\n");
    check(fh, "Failed to open file!\n");

    yaml_parser_set_input_file(&parser, fh);
    while (yaml_parser_parse(&parser, &event)) {
        switch (event.type) {
        case YAML_MAPPING_START_EVENT:
            if (output_obj == EMPTYVAL){
                output_obj = Dict_new();
            }
            break;
        case YAML_MAPPING_END_EVENT:
            break;
        case YAML_SEQUENCE_START_EVENT:
            if (output_obj == EMPTYVAL){
                output_obj = ValArray_new();
            }
            break;
        case YAML_SEQUENCE_END_EVENT:
            break;
        case YAML_SCALAR_EVENT:
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
    return output_obj;
}

int main() {
    process_yaml_file("./assets/init.yaml");
    return 0;
}
