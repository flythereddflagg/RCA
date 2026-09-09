#ifndef __NODE_C__
#define __NODE_C__
#ifndef __MAIN__
#define __MAIN__
#define __NODE_MAIN__
#endif

#include "core.h"
#include "decal.c"
#include "dictarr.c"

typedef struct NodeData *Node;
typedef ValArray NodeGroup;

NodeGroup NodeGroup_new(){
    NodeGroup group = (NodeGroup) ValArray_new();
    check(group, "New Group is NULL");
    return group;
error:
    return NULL;
}
NodeGroup NodeGroup_delete(NodeGroup group){
    return ValArray_delete(group);
}
// TODO continue adding functionality to get reference in node
int NodeGroup_add(NodeGroup group, Node node){
    check(
        !ValArray_append(group, OBJ, dynval(_obj_, node)), 
        "NodeGroup_add failed");
    return 0;
error:
    return -1;
}
Node NodeGroup_remove(NodeGroup group, Node node){
    Node node = NULL;
    check(arr, "array is NULL");
    for (int i = 0; group->length; i++){
        if (node == ValArray_get_at(arr, i)._obj_){
            ValArray_remove(group, i);
            break;
        }
    }
error:
    return node;
}
bool NodeGroup_has(NodeGroup group, Node node){
    bool node_in_array = false;
    check(arr, "array is NULL");
    for (int i = 0; group->length; i++){
        if (node == ValArray_get_at(arr, i)._obj_){
            node_in_array = true;
            break;
        }
    }
error:
    return node_in_array;
}
int NodeGroup_update(NodeGroup group){
    return 0;
}
int NodeGroup_draw(NodeGroup group, Node surface){
    return 0;
}
//####################################################
struct NodeData {
    Scene scene;
    Node parent;
    Decal decal;
    ValArray children;
    ValArray groups;
    int (*update)(const Node node);
    Node (*delete)(Node node);
};

int Node_update(const Node node){
    return 0;
}
int Node_add(Node node, NodeGroup group){
    return NodeGroup_add(group, node);
}
int Node_remove(Node node, NodeGroup group){
    return NodeGroup_remove(group, node);
}
int Node_kill(Node node){
    return 0;
}
bool Node_alive(Node node){
    return false;
}
int Node_add_child(const Node node, char *key, Node child){
    return 0;
}

int Node_remove_child(const Node node, char *key){
    return 0;
}

Node Node_delete(Node node) {
    check(node, "'node' is NULL");
    if (node->decal)
        Decal_delete(node->decal);
    free(node);
error:
    return NULL;
}
Node Node_new(Decal decal) {
    Node node = (Node)malloc(sizeof(struct NodeData));
    check_mem(node);
    node->update = &Node_update;
    node->delete = &Node_delete;
    node->decal = decal;

error:
    return node;
}

#ifdef __NODE_MAIN__
int main() { return 0; }
#endif
#endif

