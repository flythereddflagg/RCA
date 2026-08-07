#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <yaml.h>

#include "dbg.h"
#define MAX_NESTING_DEPTH 10

typedef enum { YAML_NO_STATE, YAML_MAP_STATE, YAML_SEQ_STATE } yaml_state_t;

void process_yaml_file(const char *filename) {
    FILE *fh = fopen(filename, "rb");
    yaml_state_t nests[MAX_NESTING_DEPTH] = {YAML_NO_STATE};
    yaml_parser_t parser;
    yaml_event_t event;

    check(yaml_parser_initialize(&parser),
          "Failed to initialize YAML parser!\n");

    check(fh, "Failed to open file!\n");

    yaml_parser_set_input_file(&parser, fh);
    int levels = -1;
    bool key = false; // will the next scalar be a key or a value?
    bool first_key = false;
    while (1) {
        if (!yaml_parser_parse(&parser, &event))
            break;
        switch (event.type) {
        case YAML_MAPPING_START_EVENT:
            if (nests[levels] == YAML_SEQ_STATE)
                first_key = true;
            else
                printf("\n");
            key = true; // next scalar will be a key
            levels += 1;
            nests[levels] = YAML_MAP_STATE;
            break;
        case YAML_MAPPING_END_EVENT:
            nests[levels] = YAML_NO_STATE;
            levels -= 1;
            break;
        case YAML_SEQUENCE_START_EVENT:
            printf("\n");
            levels += 1;
            nests[levels] = YAML_SEQ_STATE;
            break;
        case YAML_SEQUENCE_END_EVENT:
            key = true;
            nests[levels] = YAML_NO_STATE;
            levels -= 1;
            break;
        case YAML_SCALAR_EVENT:

            if (nests[levels] == YAML_SEQ_STATE) {
                for (int i = 0; i < levels; i++)
                    printf("  ");
                printf("- ");
                printf("%s\n", event.data.scalar.value);
            } else if (nests[levels] == YAML_MAP_STATE && key) {
                for (int i = 0; i < levels; i++)
                    printf("  ");
                if (levels > 0 && nests[levels - 1] == YAML_SEQ_STATE &&
                    first_key) {
                    printf("\b\b- ");
                    first_key = false;
                }
                printf("%s : ", event.data.scalar.value);
                key = !key;
            } else {
                printf("%s\n", event.data.scalar.value);
                key = !key;
            }
        default:
            break;
        }

        if (event.type == YAML_STREAM_END_EVENT)
            break;

        yaml_event_delete(&event);
    }

    yaml_parser_delete(&parser);
    fclose(fh);
error:
    return;
}

int main() {
    process_yaml_file("./assets/init.yaml");
    return 0;
}
