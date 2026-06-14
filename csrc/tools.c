#ifndef __TOOLS_C__
#define __TOOLS_C__
#include "cyaml.h"
#include "dbg.h"
#include "raylib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef cyaml_doc_t *Yaml;

Yaml load_yaml(const char *yaml_path) {
    char *yaml = LoadFileText(yaml_path);
    cyaml_error_t err;
    cyaml_doc_t *doc = cyaml_parse(yaml, strlen(yaml), NULL, &err);
    UnloadFileText(yaml);
    check(doc, "Parse error at line %u: %s\n", err.span.start_line, err.msg);
    return doc;

error:
    return NULL;
}
#endif
