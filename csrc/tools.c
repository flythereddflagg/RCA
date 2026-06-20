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
error:
    return doc;
}

void Yaml_delete(Yaml doc){
    if (doc)
        cyaml_free(doc);
}

DictVal Yaml_get(Yaml doc, const char *name){
    cyaml_node_t *node = NULL;
    if (strchr(name, '/'))
        node = cyaml_path(doc, name);
    else
        node = cyaml_get(doc, cyaml_root(doc), name);
    check(!cyaml_is_null_val(doc, node), "value is null");
    cyaml_scalar_kind_t type = cyaml_scalar_kind(doc, node);

    switch (type) {
        case CYAML_KIND_NULL:
            return (DictVal) {.obj=NULL};
            break;
        case CYAML_KIND_STRING:
            char* get_str = cyaml_scalar_str(doc, node);
            return (DictVal) {.str=get_str};
            break;
        case CYAML_KIND_INT:
            long get_int;
            cyaml_as_int(doc, node, &get_int);
            return (DictVal) {.num=get_int};
            break;
        case CYAML_KIND_FLOAT:
            double get_float;
            cyaml_as_float(doc, node, &get_float);
            return (DictVal) {.fnum=get_float};
            break;
        case CYAML_KIND_BOOL:
            bool get_bool;
            cyaml_as_bool(doc, node, &get_bool);
            return (DictVal) {._bool=get_bool};
            break;
        default:
            sentinel("invalid type") break;
        }
error:
    return (DictVal) {.obj=NULL};
}
#endif
