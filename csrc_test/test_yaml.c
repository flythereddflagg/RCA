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
    // int levels = 0;
    bool mapping = true;
    bool key = true;
    while (1) {
        if (!yaml_parser_parse(&parser, &event))
            break;
        if (event.type == YAML_SCALAR_EVENT && key){
            printf("Key: %s -> ", event.data.scalar.value);
            key= !key;
        }
        else if (event.type == YAML_SCALAR_EVENT){
            printf("Value: %s\n", event.data.scalar.value);
            key = !key;
        }

        if (event.type == YAML_MAPPING_START_EVENT)
            printf("\nMAPPING START\n");
        if (event.type == YAML_MAPPING_END_EVENT)
            printf("\nMAPPING END\n", event.data.scalar.value);
        if (event.type == YAML_SEQUENCE_END_EVENT)
            printf("\nSEQ END\n", event.data.scalar.value);
        if (event.type == YAML_SEQUENCE_START_EVENT)
            printf("\nSEQ START\n", event.data.scalar.value);
                

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