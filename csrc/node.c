#ifndef __NODE_C__
#define __NODE_C__
#ifndef __MAIN__
#define __MAIN__
#define __NODE_MAIN__
#endif

#include "core.h"
#include "decal.c"
#include "dict.c"
#include "valarray.c"

typedef struct NodeData *Node;
typedef ValArray NodeGroup;

struct NodeData {
    Lstring type;
    Lstring id;
    Scene scene;
    Node parent;
    Decal decal;
    Dict init;
    ValArray children;
    ValArray groups;
    int (*update)(const Node node);
    Node (*delete)(Node node);
};
int Node_update(const Node node) { return 0; }

Node Node_delete(Node node) {
    check(node, "'node' is NULL");
    if (node->decal)
        Decal_delete(node->decal);
    if (node->type.cstring)
        node->type = Lstring_delete(node->type);
    if (node->id.cstring)
        node->id = Lstring_delete(node->id);
    if (node->decal)
        node->decal = Decal_delete(node->decal);
    // NOTE this may cause issues. Maybe someone else owns init?
    if (node->init)
        node->init = Dict_delete(node->init); 
    if (node->children)
        // delete each child first?
        node->children = ValArray_delete(node->children);
    if (node->groups)
        // delete each child first?
        node->groups = ValArray_delete(node->groups);
    free(node);
error:
    return NULL;
}
Node Node_new(Scene scene, Node parent, Dict init) {
    Node node = (Node)malloc(sizeof(struct NodeData));
    check_mem(node);
    node->type = Lstring_new("Node");
    node->id = LSTRING_NULL; // TODO figure out how to use SPRINTF here?
    node->scene = scene;
    node->parent = parent;
    node->decal = NULL;
    node->init = init;
    node->children = ValArray_new();
    node->groups = ValArray_new();
    node->update = &Node_update;
    node->delete = &Node_delete;

error:
    return node;
}

NodeGroup NodeGroup_new(char *id) {
    NodeGroup group = (NodeGroup)ValArray_new();
    check(group, "New Group is NULL");
    // FIRST ELEMENT IS ALWAYS A STRING WITH THE GROUP ID
    check(!ValArray_append(group, STR, dynval(_str_, Lstring_new(id))),
          "ID append failed");
error:
    return group;
}
NodeGroup NodeGroup_delete(NodeGroup group) {
    check(group, "Group to be deleted is NULL");
    Node current = NULL;
    // starting at 1 because first element is always the string ID
    for (int i = 1; i < group->length; i++) {
        current = (Node)ValArray_get_at(group, i)._obj_;
        current->delete (current);
        ValArray_set_at(group, i, NONE, EMPTYVAL);
    }
error:
    return ValArray_delete(group);
}

int NodeGroup_add(NodeGroup group, Node node) {
    check(!ValArray_append(group, OBJ, dynval(_obj_, node)),
          "NodeGroup_add failed");
    check(!ValArray_append(node->groups, OBJ, dynval(_obj_, group)),
          "Node_add failed");
    return 0;
error:
    return -1;
}
Node NodeGroup_remove(NodeGroup group, Node node) {
    Node matched_node = NULL;
    NodeGroup matched_nodegroup = NULL;
    check(group, "group is NULL");
    check(node, "node is NULL");
    for (int i = 0; group->length; i++) {
        if (node == (Node)ValArray_get_at(group, i)._obj_) {
            matched_node = (Node)ValArray_remove(group, i)._obj_;
            break;
        }
    }
    check(matched_node, "node not found!");
    for (int i = 0; node->groups->length; i++) {
        if (group == (NodeGroup)ValArray_get_at(node->groups, i)._obj_) {
            matched_nodegroup =
                (NodeGroup)ValArray_remove(node->groups, i)._obj_;
            break;
        }
    }
    check(matched_nodegroup, "group in node not found");
error:
    return matched_node;
}
bool NodeGroup_has(NodeGroup group, Node node) {
    bool node_in_array = false;
    check(group, "group is NULL");
    for (int i = 0; group->length; i++) {
        if (node == ValArray_get_at(group, i)._obj_) {
            node_in_array = true;
            break;
        }
    }
error:
    return node_in_array;
}
int NodeGroup_update(NodeGroup group) {
    check(group, "group is NULL");
    Node current = NULL;

    // starting at 1 because first element is always the string ID
    for (int i = 1; i < group->length; i++) {
        current = (Node)ValArray_get_at(group, i)._obj_;
        current->update(current);
    }
    return 0;
error:
    return -1;
}
int NodeGroup_draw(NodeGroup group, Node surface) { return 0; }
// ####################################################


int Node_add(Node node, NodeGroup group) { return NodeGroup_add(group, node); }
Node Node_remove(Node node, NodeGroup group) {
    return NodeGroup_remove(group, node);
}
int Node_kill(Node node) {
    Node current = NULL;
    for (int i = 0; i < node->groups->length; i++) {
        current = NodeGroup_remove(
            (NodeGroup)ValArray_get_at(node->groups, i)._obj_, node);
    }
    check(current, "Node Not removed from any NodeGroups");
    return 0;
error:
    return -1;
}
bool Node_alive(Node node) {
    for (int i = 0; i < node->groups->length; i++) {
        if (NodeGroup_has((NodeGroup)ValArray_get_at(node->groups, i)._obj_,
                          node))
            return true;
    }
    check(!node->groups->length, "NODE-NODEGROUP inconsistency");
error:
    return false;
}
// TODO continue here and add tests
int Node_add_child(const Node node, char *key, Node child) { return 0; }

int Node_remove_child(const Node node, char *key) { return 0; }


#ifdef __NODE_MAIN__
int main() { 
    Node node = Node_new(NULL, NULL, Dict_new());
    node = Node_delete(node);
    return 0; 
}
#endif
#endif
