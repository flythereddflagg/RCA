
#include "decal.h"
int Decal_setup(Node node) {
    check(node, "Node is NULL");
    check(Lstring_equal(node->type, to_Lstring("Decal")),
          "Node->type is '" LSTRING_FMT "', not Decal",
          Lstring_format(node->type));
    check(node->sprite, "Node sprite is NULL");
    
    return 0;
error:
    return -1;
}
Node Decal_delete(Node node) { return NULL; }
int Decal_update(Node node) { return 0; }
