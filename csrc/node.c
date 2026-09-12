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
    Scene scene;
    Node parent;
    Decal decal;
    ValArray children;
    ValArray groups;
    int (*update)(const Node node);
    Node (*delete)(Node node);
};

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

int Node_update(const Node node) { return 0; }
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
