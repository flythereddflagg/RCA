#ifndef __NODE_C__
#define __NODE_C__
#ifndef __MAIN__
#define __MAIN__
#define __NODE_MAIN__
#endif

#include "core.h"
#include "dict.c"
#include "sprite.c"
#include "objlist.c"

#define INHERIT_KEY "_inherit_"
#define MISSING_TYPE "<MISSING TYPE>"

typedef struct NodeData *Node;
typedef ObjList NodeGroup;
typdef ObjList GroupList;



struct NodeData {
    Lstring type;
    Lstring id;
    Scene scene;
    Node parent;
    Sprite sprite;
    Dict init;
    NodeGroup children;
    NodeGroup *groups;
    size_t groups_length;
    int (*update)(const Node node);
    Node (*delete)(Node node);
};

Node Node_delete(Node node);
Node Node_kill(Node node);
Node Node_new();

NodeGroup NodeGroup_new() {
    return ObjList_new();
}
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
    return NULL
}
int NodeGroup_add(NodeGroup group, Node node) {
    check(group, "group is NULL");
    check(node, "node is NULL");
    // CONTINUE HERE WITH THE OBJLISTS
    group->nodes[group->length] = node;
    group->length++;

    node->groups[node->groups_length] = group;
    node->groups_length++;
    return 0;
error:
    return -1;
}

Node NodeGroup_remove(NodeGroup group, Node node) {
    Node matched_node = NULL;
    NodeGroup matched_nodegroup = NULL;
    check(group && group->nodes, "invalid group");
    check(node && node->groups, "invalid node");
    for (size_t i = 0; i < group->length; i++) {
        if (node == group->nodes[i]) {
            matched_node = node;
            group->nodes[i] = NULL;
            for (size_t j = i; j < group->length - 1; j++) {
                group->nodes[i] = group->nodes[i + 1];
            }
            group->nodes[group->length] = NULL;
            group->length--;
            break;
        }
    }
    check(matched_node, "node not found!");
    for (size_t i = 0; i < node->groups_length; i++) {
        if (group == node->groups[i]) {
            matched_group = group;
            node->groups[i] = NULL;
            for (size_t j = i; j < node->groups_length - 1; j++) {
                node->groups[i] = node->groups[i + 1];
            }
            node->groups[node->groups_length] = NULL;
            node->groups_length--;
            break;
        }
    }
    check(matched_nodegroup, "group in node not found");
error:
    return matched_node;
}
// TODO update the code to NOT use a valarray CONTINUE HERE
bool NodeGroup_has(NodeGroup group, Node node) {
    bool node_in_array = false;
    check(group, "group is NULL");
    for (size_t i = 0; i < group->length; i++) {
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
    for (size_t i = 0; i < group->length; i++) {
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
    // owned field?
    node->init = NULL;
    node->children = ValArray_new(); // dtype=Node
    node->groups = ValArray_new();   // dtype=NodeGroup
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
        for (size_t i = 0; i < node->children->length; i++) {
            child = (Node)ValArray_remove(node->children, -1)._obj_;
            child->delete (child);
        }
        node->children = ValArray_delete(node->children);
    }
    if (node->groups) {
        node->groups = ValArray_delete(node->groups);
    }
    // if (node->init)
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
    NodeGroup group = NULL;
    Node current = NULL;
    Node child = NULL;
    check(node->groups, "node->groups is NULL");
    check_debug(node->groups->length > 0, "node is not in any groups");
    size_t groups_length = node->groups->length;
    for (size_t i = 0; i < groups_length; i++) {
        group = ValArray_remove(node->groups, -1)._obj_;
        debug("group %p, length = %d", group, group->length);
        check(group->length < 1000 && group->length > 0,
              "WHAAAAT?") for (size_t j = 0; j < group->length; j++) {
            // debug("%d", j);
            if (node == (Node)ValArray_get_at(group, j)._obj_) {
                current = (Node)ValArray_remove(group, j)._obj_;
                break;
            }
        }
    }
    check(current, "Node Not removed from any NodeGroups");
    // if you kill a parent. Kill all children too.
    for (size_t i = 0; i < node->children->length; i++) {
        child = (Node)ValArray_get_at(node->children, i)._obj_;
        Node_kill(child);
    }

error:
    return node;
}
bool Node_alive(Node node) {
    for (size_t i = 0; i < node->groups->length; i++) {
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
    for (size_t i = 0; i < node->children->length; i++) {
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
    for (size_t i = 0; i < node->children->length; i++) {
        if (child == (Node)ValArray_get_at(node->children, i)._obj_) {
            return (Node)ValArray_remove(node->children, i)._obj_;
        }
    }
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
    debug("killing node");
    Node_kill(node);
    debug("group->length: %d", group->length);
    debug("group2->length: %d", group2->length);
    group = NodeGroup_delete(group);
    group2 = NodeGroup_delete(group2);
    return 0;
}
#endif
#endif
