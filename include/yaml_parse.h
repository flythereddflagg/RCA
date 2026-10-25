#ifndef __YAML_PARSE_H__
#define __YAML_PARSE_H__
#include "dbg.h"
#include "dict.h"
#include "lstring.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <yaml.h>
#define MAX_NESTING_DEPTH 10
typedef enum { YAML_NO_STATE, YAML_MAP_STATE, YAML_SEQ_STATE } yaml_state_t;
typedef struct {
    DynValue value;
    DynType type;
} DynTypeVal;

DynTypeVal YamlParse_parse_value(yaml_event_t event);
DynValue YamlParse_process_yaml_file(const char *filename);
int test_dict();
int test_init();

#endif
