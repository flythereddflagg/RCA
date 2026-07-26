#ifndef __YAML_C__
#define __YAML_C__
#ifndef __MAIN__
#define __MAIN__
#define __YAML_MAIN__
#endif
#include "cyaml.h"
#include "dbg.h"
#include "dictarr.c"
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

Yaml Yaml_delete(Yaml doc) {
    if (doc)
        cyaml_free(doc);
    return NULL;
}

DynValue Yaml_get(Yaml doc, const char *name) {
    cyaml_node_t *node = NULL;
    if (strchr(name, '/'))
        node = cyaml_path(doc, name);
    else
        node = cyaml_get(doc, cyaml_root(doc), name);
    // check(!cyaml_is_null_val(doc, node), "key: %s; value is null", name);
    cyaml_scalar_kind_t type = cyaml_scalar_kind(doc, node);

    switch (type) {
    case CYAML_KIND_NULL:
        return (DynValue){._obj_ = NULL};
        break;
    case CYAML_KIND_STRING:
        char *get_str = cyaml_scalar_str(doc, node);
        return (DynValue){._str_ = get_str};
        break;
    case CYAML_KIND_INT:
        long get_int;
        cyaml_as_int(doc, node, &get_int);
        return (DynValue){._int_ = get_int};
        break;
    case CYAML_KIND_FLOAT:
        double get_float;
        cyaml_as_float(doc, node, &get_float);
        return (DynValue){._float_ = get_float};
        break;
    case CYAML_KIND_BOOL:
        bool get_bool;
        cyaml_as_bool(doc, node, &get_bool);
        return (DynValue){._bool_ = get_bool};
        break;
    default:
        sentinel("invalid type") break;
    }
error:
    return (DynValue){._obj_ = NULL};
}
#endif
#ifdef __YAML_MAIN__
int main() {
    Yaml settings = Yaml_load("./assets/init.yaml");
    check(settings, "yaml could not load");
    log_info("%d", Yaml_get(settings, "FPS")._int_);
    log_info("%d", Yaml_get(settings, "SHOW_EVENTS")._bool_);
    log_info("%d", Yaml_get(settings, "/ASPECT_RATIO[1]")._int_);
    log_info("%s", Yaml_get(settings, "icon")._str_);
    log_info("%s", Yaml_get(settings, "title")._str_);
    log_info("%p", Yaml_get(settings, "/new_game_add_in[0]/groups")._obj_);
    Yaml_delete(settings);
    return 0;
error:
    return 1;
}
#endif
