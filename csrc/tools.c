#ifndef __TOOLS_C__
#define __TOOLS_C__
#include "cyaml.h"
#include "dict.c"
#include "dbg.h"
#include "raylib.h"
#include <stdlib.h>
#include <string.h>

typedef cyaml_doc_t *Yaml;

Yaml Yaml_load(const char *yaml_path) {
    char *yaml = LoadFileText(yaml_path);
    cyaml_error_t err;
    cyaml_doc_t *doc = cyaml_parse(yaml, strlen(yaml), NULL, &err);
    UnloadFileText(yaml);
    check(doc, "Parse error at line %u: %s\n", err.span.start_line, err.msg);
    return doc;

error:
    return NULL;
}
DictVal Yaml_get(Yaml doc, DictType type, const char *name){
    cyaml_node_t* node = cyaml_get(doc, cyaml_root(doc), name);
    check(!cyaml_is_null_val(doc, node), "value is null");
    switch (type) {
        case NONE:
            return (DictVal) {.obj=NULL};
            break;
        case DICT:
            sentinel("DICT not yet implemented");
            break;
        case ARR:
            sentinel("ARR not yet implemented");
            break;
        case STR:
            char* get_str = cyaml_scalar_str(doc, node);
            return (DictVal) {.str=get_str};
            break;
        case INT:
            long get_int;
            cyaml_as_int(doc, node, &get_int);
            return (DictVal) {.num=get_int};
            break;
        case FLOAT:
            double get_float;
            cyaml_as_int(doc, node, &get_float);
            return (DictVal) {.fnum=get_float};
            break;
        case BOOL:
            bool get_bool;
            cyaml_as_int(doc, node, &get_bool);
            return (DictVal) {._bool=get_bool};
            break;
        case OBJ:
            sentinel("OBJ not yet implemented");
            break;
        default:
            sentinel("invalid type") break;
        }
error:
    return (DictVal) {.obj=NULL};
}
#endif
