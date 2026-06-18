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
DictVal Yaml_get(DictType type, const char *name){
    cyaml_as_int(
        settings, 
        cyaml_get(settings, cyaml_root(settings), "RESOLUTION"),
        &resolution
    
    );
    switch (dict->types[i]) {
        case NONE:
            printf(" none %20s", "null");
            break;
        case DICT:
            Dict_printrepr(dict->vals[i].dict);
            break;
        case ARR:
        case STR:
            printf("  str %20s", dict->vals[i].str);
            break;
        case INT:
            printf("  int %20lld", dict->vals[i].num);
            break;
        case FLOAT:
            printf("float %20f", dict->vals[i].fnum);
            break;
        case BOOL:
            printf(" bool %20d", dict->vals[i]._bool);
            break;
        case OBJ:
            printf("  obj %20p", dict->vals[i].obj);
            break;
        default:
            sentinel("invalid type") break;
        }
        if (dict->next[i] == NO_NEXT)
            printf(" | null\n");
        else
            printf(" | %d\n", dict->next[i]);
    }
error:
    return (DictVal) {.num=0};
}
#endif
