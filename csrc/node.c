#ifndef __NODE_C__
#define __NODE_C__
#include "dbg.h"
#include "decal.c"
#include "raylib.h"
#include <stdio.h>
#include <stdlib.h>
#define MAX_NODES 256
#define ID_SIZE 32
#define ID_MAX 255
/*
TODO Node still needs the following:
children
groups
*/
typedef struct NodeData *Node;
typedef struct {
    unsigned char len;
    Node *arr;
} NodeArray;

void NodeArray_add_node(NodeArray *nodes, Node node) {
    if (nodes->len >= MAX_NODES)
        return;
    nodes->arr[nodes->len] = node;
    nodes->len += 1;
}

struct NodeData {
    void *scene;
    void *parent;
    Decal decal;
    void *children;
    void (*update)(const void *self);
    void (*delete)(Node self);
};

void Node_update(const void *self) { ; }

void Node_delete(Node self) {
    check(self, "'self' is NULL");
    if (self->decal)
        self->decal->delete(self->decal);
    free(self);
error:;
}

void Node_add_child(const void *self, void *child);

void Node_remove_child(const void *self, void *child);

Node Node_new(Decal decal) {
    Node self = (Node)malloc(sizeof(struct NodeData));
    check_mem(self);
    self->update = &Node_update;
    self->delete = &Node_delete;
    self->decal = decal;

error:
    return self;
}

#endif
