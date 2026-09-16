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
    Decal sprite;
    Dict init;
    ValArray children;
    ValArray groups;
    int (*update)(const Node node);
    Node (*delete)(Node node);
};

Node Node_delete(Node node);

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

Node Node_new() {
    Node node = (Node)malloc(sizeof(struct NodeData));
    check_mem(node);
    // owned field
    node->type = LSTRING_NULL; // NULL is uninitialized node i guess
    // owned field
    node->id = LSTRING_NULL; // TODO figure out how to use SPRINTF here?
    node->scene = NULL;
    node->parent = NULL;
    // owned field
    node->sprite = NULL;
    // owned field
    node->init = NULL;
    node->children = ValArray_new();
    node->groups = ValArray_new();
    node->update = &Node_update;
    node->delete = &Node_delete;

error:
    return node;
}
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
    check_debug(current, "Node Not removed from any NodeGroups");
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
int Node_add_child(const Node node, Node child) {
    check(node, "given node is NULL");
    check(child, "given id is NULL");
    child->parent = node;
    check(!ValArray_append(node->children, OBJ, dynval(_obj_, child)),
          "add child failed");
    return 0;
error:
    return -1;
}

Node Node_child_by_id(Node node, char *id) {
    check(node, "given node is NULL");
    check(id, "given id is NULL");
    Lstring id_string = Lstring_new(id);
    for (int i = 0; i < node->children->length; i++) {
        if (Lstring_equal(
                id_string,
                ((Node)ValArray_get_at(node->children, i)._obj_)->id)) {
            id_string = Lstring_delete(id_string);
            return (Node)ValArray_get_at(node->children, i)._obj_;
        }
    }
error:
    id_string = Lstring_delete(id_string);
    return NULL;
}

Node Node_remove_child(const Node node, Node child) {
    check(node, "given node is NULL");
    check(child, "given id is NULL");
    for (int i = 0; i < node->children->length; i++) {
        if (child == (Node)ValArray_get_at(node->children, i)._obj_) {
            return (Node)ValArray_remove(node->children, i)._obj_;
        }
    }
error:
    return NULL;
}
Node Node_delete(Node node) {
    check(node, "'node' is NULL");
    if (node->groups) {
        Node_kill(node);
        node->groups = ValArray_delete(node->groups);
    }
    if (node->children) {
        Node child = NULL;
        for (int i = 0; i < node->children->length; i++) {
            child = (Node)ValArray_get_at(node->children, i)._obj_;
            ValArray_set_at(node->children, i, NONE,
                            dynval(_obj_, child->delete (child)));
        }
        node->children = ValArray_delete(node->children);
    }
    if (node->init)
        node->init = Dict_delete(node->init);
    if (node->sprite)
        Decal_delete(node->sprite);
    if (node->id.cstring)
        node->id = Lstring_delete(node->id);
    if (node->type.cstring)
        node->type = Lstring_delete(node->type);
    free(node);
error:
    return NULL;
}
#ifdef __NODE_MAIN__
int main() {
    NodeGroup group = NodeGroup_new("cheesy boi");

    Node node = Node_new();
    Node_add_child(node, Node_new());
    Node_add(node, group);
    group = NodeGroup_delete(group);
    return 0;
}
#endif
#endif
