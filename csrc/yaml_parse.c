#ifndef __YAML_PARSE_C__
#define __YAML_PARSE_C__
#ifndef __MAIN__
#define __MAIN__
#define __YAML_PARSE_MAIN__
#endif
#include <ctype.h>
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

typedef struct {
    DynValue value;
    DynType type;
} DynTypeVal;

DynTypeVal YamlParse_parse_value(yaml_event_t event) {
    /*
    check that the value is not 0 if it is return int = 0
    try to parse as a int and a float. If int and float are the same value and
    there is no e, E or '.' in the string, parse as int, otherwise parse as
    float (use --strtol and strtof--) if parsing error occurs then check for
    bool lower("true") and lower("false") only if all of these fail do you parse
    as string
    */
    Lstring event_value = Lstring_new((char *)event.data.scalar.value);
    Lstring val_copy = Lstring_new(event_value.cstring);

    DynValue value = EMPTYVAL;
    DynType type = NONE;
    int i_val = (int)strtol(event_value.cstring, NULL, 0);
    float f_val = strtof(event_value.cstring, NULL);
    if (Lstring_cstring_equal("0", event_value.cstring)) {
        value = dynval(_int_, 0);
        Lstring_delete(event_value);
    } else {
        if (i_val == 0 && f_val == 0.0f) { // so not a number

            for (size_t i = 0; i < val_copy.length; i++)
                val_copy.cstring[i] = (char)tolower(val_copy.cstring[i]);

            if (Lstring_cstring_equal("true", val_copy.cstring)) {
                value = dynval(_bool_, true);
                type = BOOL;
                Lstring_delete(event_value);
            } else if (Lstring_cstring_equal("false", val_copy.cstring)) {
                value = dynval(_bool_, false);
                type = BOOL;
                Lstring_delete(event_value);
            } else {
                if (Lstring_cstring_equal("", event_value.cstring)) {
                    value = dynval(_obj_, NULL);
                    type = NONE;
                    Lstring_delete(event_value);
                } else {
                    value = dynval(_str_, event_value);
                    type = STR;
                    // DO NOT DELETE IF ITS A STRING
                    // Lstring_delete(event_value);
                }
            }

        } else if ((float)i_val == f_val && !strchr(event_value.cstring, 'e') &&
                   !strchr(event_value.cstring, 'e') &&
                   !strchr(event_value.cstring, '.')) {
            value = dynval(_int_, i_val);
            type = INT;
            Lstring_delete(event_value);
        } else {
            value = dynval(_float_, f_val);
            type = FLOAT;
            Lstring_delete(event_value);
        }
    }
    Lstring_delete(val_copy);
    return (DynTypeVal){.value = value, .type = type};
}

DynValue YamlParse_process_yaml_file(const char *filename) {
    DynValue cur_obj = EMPTYVAL;
    DynValue out_obj = EMPTYVAL;
    int top = -1, fail = 0;
    Lstring cur_key = LSTRING_NULL;
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
                fail =
                    Dict_set(stack[top]._dict_, cur_key.cstring, DICT, cur_obj);
                check(!fail, "Dict failure detected");
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
                fail =
                    Dict_set(stack[top]._dict_, cur_key.cstring, ARR, cur_obj);
                check(!fail, "Dict failure detected");
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
            key = true;
            break;
        case YAML_SCALAR_EVENT:
            if (levels[top] == YAML_SEQ_STATE) {
                DynTypeVal type_value = YamlParse_parse_value(event);
                ValArray_append(stack[top]._arr_, type_value.type,
                                type_value.value);
            } else if (levels[top] == YAML_MAP_STATE && key) {

                cur_key = Lstring_set(cur_key, (char *)event.data.scalar.value);
                key = !key;
            } else {
                DynTypeVal type_value = YamlParse_parse_value(event);
                fail = Dict_set(stack[top]._dict_, cur_key.cstring,
                                type_value.type, type_value.value);
                check(!fail, "Dict failure detected");
                key = !key;
            }
            break;
        default:
            // debug("NO PARSABLE EVENT");
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
#endif
#ifdef __YAML_PARSE_MAIN__
int main() {
    DynValue out = YamlParse_process_yaml_file("./assets/init.yaml");
    Dict dict = out._dict_;
    log_info("FINAL DICT");
    Dict_print(out._dict_);
    printf("\n");
    ValArray aspect_ratio_parts = Dict_get(
        dict, "ASPECT_RATIO", EMPTYVAL)._arr_;
    check(aspect_ratio_parts, "ValArray Failed to load.");
    
    Dict_delete(out._dict_);
    return 0;

error:
    Dict_delete(out._dict_);
}
#endif
