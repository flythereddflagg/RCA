#ifndef __NODE_H__
#define __NODE_H__
#include "objlist.h"
#include "dict.h"
typedef ObjList NodeGroup;
typedef ObjList GroupList;
typedef struct NodeData *Node;
typedef int (*NodeFunc)(Node node);
typedef struct {
    char *key;
    NodeFunc func;
} KeyFuncPair;


#define MAX_KEY_LEN 100
#define kf_pair(k, f)                                                          \
    (KeyFuncPair) { .key = k, .func = f }

typedef int (*NodeFunc)(Node node);
typedef struct {
    char *key;
    NodeFunc func;
} KeyFuncPair;
int Node_setup(Node node);
NodeGroup NodeGroup_new();
NodeGroup NodeGroup_delete(NodeGroup group);
int NodeGroup_add(NodeGroup group, Node node);
Node NodeGroup_remove(NodeGroup group, Node node);
bool NodeGroup_has(NodeGroup group, Node node);
int NodeGroup_update(NodeGroup group);
int NodeGroup_draw(NodeGroup group, Node surface);
int Node_update(const Node node);
Node Node_new();
Node Node_delete(Node node);
int Node_add(Node node, NodeGroup group);
Node Node_remove(Node node, NodeGroup group);
Node Node_kill(Node node);
bool Node_alive(Node node);
int Node_add_child(const Node node, Node child);
int Node_setup_children(Node node);
Node Node_child_by_id(Node node, char *id);
Node Node_remove_child(const Node node, Node child);
NodeFunc Node_get_setup(char *key);
Node Node_from_dict(Dict init);
int test_node_from_dict();

#endif
