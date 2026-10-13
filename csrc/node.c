#ifndef __NODE_C__
#define __NODE_C__
#ifndef __MAIN__
#define __MAIN__
#define __NODE_MAIN__
#endif

#include "core.h"
#include "dict.c"
#include "lstring.c"
#include "objlist.c"
#include "sprite.c"

#define INHERIT_KEY "_inherit_"
#define MISSING_TYPE "<MISSING TYPE>"
#define MISSING_ID "<NO ID>"

typedef struct NodeData *Node;
typedef ObjList NodeGroup;
typedef ObjList GroupList;

struct NodeData {
    Lstring type;
    Lstring id;
    Scene scene;
    Node parent;
    Sprite sprite;
    Dict init;
    NodeGroup children;
    GroupList groups;
    size_t groups_length;
    int (*update)(const Node node);
    Node (*delete)(Node node);
};

Node Node_delete(Node node);
Node Node_kill(Node node);
Node Node_new();

NodeGroup NodeGroup_new() { return ObjList_new(); }
NodeGroup NodeGroup_delete(NodeGroup group) {
    check(group, "Group to be deleted is NULL");
    Node current = NULL;
    size_t length = group->length;
    for (size_t i = 0; i < length; i++) {
        current = ObjList_at(group, i);
        ObjList_set_at(group, i, current->delete (current));
    }
    return ObjList_delete(group);
error:
    return NULL;
}
int NodeGroup_add(NodeGroup group, Node node) {
    check(group, "group is NULL");
    check(node, "node is NULL");
    check(!ObjList_push(group, node), "group add failed");
    check(!ObjList_push(node->groups, group), "node add group failed");
    return 0;
error:
    return -1;
}

Node NodeGroup_remove(NodeGroup group, Node node) {
    check(group, "group is NULL");
    check(node, "node is NULL");
    Node out = (Node)ObjList_remove(group, node);
    check(!out, "group remove failed");
    check(!ObjList_remove(node->groups, group), "node remove group failed.");
    return out;
error:
    return NULL;
}
bool NodeGroup_has(NodeGroup group, Node node) {
    return ObjList_has(group, node);
}
int NodeGroup_update(NodeGroup group) {
    check(group, "group is NULL");
    Lnode current = group->head;
    Node node = NULL;
    for (size_t i = 0; i < group->length; i++) {
        check(current, "current Lnode is NULL at postition %lu", i);
        node = (Node)current->obj;
        check(!node->update(node), "Node <" LSTRING_FMT "> failed to update",
              Lstring_format(node->id));
        current = current->next;
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
    node->type = to_Lstring(MISSING_TYPE);
    // owned field
    node->id = to_Lstring(MISSING_ID);
    node->scene = NULL;
    node->parent = NULL;
    // owned field
    node->sprite = NULL;
    // owned field?
    node->init = NULL;
    node->children = ObjList_new(); // dtype=Node
    node->groups = ObjList_new();   // dtype=NodeGroup
    node->update = &Node_update;
    node->delete = &Node_delete;

error:
    return node;
}
Node Node_delete(Node node) {
    check(node, "'node' is NULL");
    if (node->groups) {
        Node_kill(node);
    }
    if (node->children) {
        Node child = NULL;
        size_t length = node->children->length;
        for (size_t i = 0; i < length; i++) {
            child = (Node)ObjList_pop(node->children);
            child->delete (child);
        }
        node->children = ObjList_delete(node->children);
    }
    if (node->groups) {
        node->groups = ObjList_delete(node->groups);
    }
    // if (node->init) // do NOT delete because node does not own it
    //     node->init = Dict_delete(node->init);
    if (node->sprite)
        Sprite_delete(node->sprite);
    if (node->id.cstring) {
        node->id = Lstring_delete(node->id);
    }
    if (node->type.cstring) {
        node->type = Lstring_delete(node->type);
    }

    free(node);
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
int Node_add(Node node, NodeGroup group) { return NodeGroup_add(group, node); }
Node Node_remove(Node node, NodeGroup group) {
    return NodeGroup_remove(group, node);
}
Node Node_kill(Node node) {
    check(node, "node is NULL");
    check(node->groups, "node->groups is NULL");
    check_debug(node->groups->length > 0, "node is not in any groups");
    size_t groups_length = node->groups->length;
    NodeGroup group = NULL;
    for (size_t i = 0; i < groups_length; i++) {
        group = ObjList_pop(node->groups);
        check(ObjList_remove(group, node), "group remove failed");
    }
    check_debug(group, "Node Not removed from any NodeGroups");
    // if you kill a parent. Kill all children too.
    Node child = NULL;
    Lnode current = node->children->head;
    for (size_t i = 0; i < node->children->length; i++) {
        check(current, "current is NULL at postition %lu", i);
        child = (Node)current->obj;
        Node_kill(child);
        current = current->next;
    }
error:
    return node;
}
bool Node_alive(Node node) {
    check(node, "Node is NULL");
    check(node->groups, "Node groups is NULL");
    return node->groups->length ? true : false;
error:
    return false;
}
int Node_add_child(const Node node, Node child) {
    check(node, "given node is NULL");
    check(child, "given id is NULL");
    child->parent = node;
    check(!ObjList_push(node->children, child), "add child failed");
    return 0;
error:
    return -1;
}

Node Node_child_by_id(Node node, char *id) {
    check(node, "given node is NULL");
    check(id, "given id is NULL");
    Lstring id_string = Lstring_new(id);
    Lnode current = node->children->head;
    Node child = NULL;
    for (size_t i = 0; i < node->children->length; i++) {
        check(current, "current is NULL at postition %lu", i);
        child = current->obj;
        check(child, "child is NULL at position %lu", i);
        if (Lstring_equal(id_string, child->id)) {
            id_string = Lstring_delete(id_string);
            return child;
        }
        current = current->next;
    }
    sentinel("Child with id '" LSTRING_FMT "'not found!",
             Lstring_format(child->id));
error:
    id_string = Lstring_delete(id_string);
    return NULL;
}

Node Node_remove_child(const Node node, Node child) {
    check(node, "given node is NULL");
    check(child, "given id is NULL");
    return (Node)ObjList_remove(node->children, child);
error:
    return NULL;
}

#ifdef __NODE_MAIN__
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
    node->delete(node);
    return 0;
}
#endif
#endif
