#ifndef __NODE_FROM_DICT_C__
#define __NODE_FROM_DICT_C__
#ifndef __MAIN__
#define __MAIN__
#define __NODE_FROM_DICT_MAIN__
#endif

#include <string.h>

#include "core.h"
#include "dict.c"
#include "lstring.c"
#include "node.c"
#define kf_pair(k, f)                                                          \
    (KeyFuncPair) { .key = k, .func = f }

typedef int (*func)(Node node) NodeFunc;
typedef struct {
    char *key;
    NodeFunc func;
} KeyFuncPair;

KeyFuncPair SETUP_FUNCS[] = {
    kf_pair("Node", Node_setup),
    kf_pair("Animation", Node_setup),
    kf_pair("Backpack", Node_setup),
    kf_pair("Cactus", Node_setup),
    kf_pair("Camera", Node_setup),
    kf_pair("Coin", Node_setup),
    kf_pair("CutScene", Node_setup),
    kf_pair("Decal", Node_setup),
    kf_pair("Edge", Node_setup),
    kf_pair("Gate", Node_setup),
    kf_pair("Item", Node_setup),
    kf_pair("Menu", Node_setup),
    kf_pair("Music", Node_setup),
    kf_pair("OpenUrlTrigger", Node_setup),
    kf_pair("Retry", Node_setup),
    kf_pair("SFX", Node_setup),
    kf_pair("SoftDirt", Node_setup),
    kf_pair("TextBox", Node_setup),
    kf_pair("TextRoll", Node_setup),
    kf_pair("Trigger", Node_setup)
};

size_t SETUP_FUNCS_SIZE = sizeof(SETUP_FUNCS) / sizeof(KeyFuncPair);

NodeFunc Node_get_setup(char *key){
    check(key, "key is NULL");
    
error:
    return NULL;
}

Node Node_from_dict(Dict init) {
    Dict yaml = Dict_get(init, "yaml", EMPTYVAL)._dict_;
    if (yaml) {
        ;
        // TODO write code to overwrite the data in yaml with the data in init
    }
    Node node = Node_new();
    check(node, "node from dict failed");
    node->init = init;
    
    return node;
error:
    return NULL;
}

#ifdef __NODE_FROM_DICT_MAIN__
int main() {
    NodeGroup group = NodeGroup_new();
    NodeGroup group2 = NodeGroup_new();

    Node node = Node_new();
    debug("deleting node");
    node = node->delete (node);
    debug("remaking node");
    node = Node_new();
    Node_add_child(node, Node_new());

    Node_add(node, group);
    NodeGroup_add(group2, node);
    NodeGroup_add(group, (Node)ObjList_at(node->children, 0));
    debug("group->length: %lu", group->length);
    debug("group2->length: %lu", group2->length);
    debug("killing node");
    node = Node_kill(node);
    debug("group->length: %lu", group->length);
    debug("group2->length: %lu", group2->length);
    group = NodeGroup_delete(group);
    group2 = NodeGroup_delete(group2);
    node->delete (node);
    return 0;
}
#endif
#endif
