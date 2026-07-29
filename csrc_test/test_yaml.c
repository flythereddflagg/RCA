#include <yaml.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "dbg.h"


void process_yaml_file(const char *filename) {
    FILE *fh = fopen(filename, "rb");
    yaml_parser_t parser;
    yaml_event_t event;

    check(
        yaml_parser_initialize(&parser), 
        "Failed to initialize YAML parser!\n");

    check(fh, "Failed to open file!\n");

    yaml_parser_set_input_file(&parser, fh);
    int levels = 0;
    bool key = false;
    bool seq = false;
    while (1) {
        if (!yaml_parser_parse(&parser, &event))
            break;
        switch (event.type){
            case YAML_MAPPING_START_EVENT:
                key = true;
                printf("\n");
                levels += 1;
                break;
            case YAML_MAPPING_END_EVENT:
                // key = false;
                printf("\n");
                levels -= 1;
                break;
            case YAML_SEQUENCE_START_EVENT:
                seq = true;
                printf("\n");
                levels += 1;
                break;
            case YAML_SEQUENCE_END_EVENT:
                seq = false;
                printf("\n");
                levels -= 1;
                break;
            case YAML_SCALAR_EVENT:
                for (int i = 0; i < levels; i++)
                    printf("  ");
                if (seq)
                    printf(" - ");
                if (key){
                    printf("%s -> ", event.data.scalar.value);
                    key= !key;
                }
                else {
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