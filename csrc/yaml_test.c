#include "cyaml.h"
#include "dbg.h"
#include "raylib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    const char *yaml = LoadFileText("./assets/init.yaml");
    cyaml_error_t err;
    cyaml_doc_t *doc = cyaml_parse(yaml, strlen(yaml), NULL, &err);

    check(doc, "Parse error at line %u: %s\n", err.span.start_line, err.msg);

    cyaml_node_t *root = cyaml_root(doc);

    char *value = cyaml_scalar_str(doc, cyaml_get(doc, root, "icon"));
    printf("icon: %s\n", value);
    free(value);

    cyaml_free(doc);
    return 0;

error:
    return 1;
}
