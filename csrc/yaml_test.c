#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "cyaml.h"

int main(){
    const char *yaml = "name: cyaml\nversion: 1.0\n";
    cyaml_error_t err;
    cyaml_doc_t *doc = cyaml_parse(yaml, strlen(yaml), NULL, &err);

    if (!doc) {
        fprintf(stderr, "Parse error at line %u: %s\n", err.span.start_line, err.msg);
        return 1;
    }

    cyaml_node_t *root = cyaml_root(doc);
    cyaml_node_t *name = cyaml_get(doc, root, "name");

    char *value = cyaml_scalar_str(doc, name);
    printf("name: %s\n", value);
    free(value);

    cyaml_free(doc);
    return 0;
}