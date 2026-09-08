#ifndef __NODE_C__
#define __NODE_C__
#ifndef __MAIN__
#define __MAIN__
#define __NODE_MAIN__
#endif

// #include "core.h"
#include "decal.c"
// #include "dictarr.c"
// #include "raylib.h"
// #include <stdio.h>
// #include <stdlib.h>
#define MAX_NODES 256
#define ID_SIZE 32
#define ID_MAX 255
/*
TODO Node still needs the following:
children
groups
*/
typedef struct NodeData *Node;
typedef ValArray NodeGroup;

void NodeGroup_new(void);
void NodeGroup_delete(void);
void NodeGroup_nodes(void);
void NodeGroup_add(void);
void NodeGroup_remove(void);
void NodeGroup_has(void); // or IN?
void NodeGroup_update(void);
void NodeGroup_draw(void);

void Node_add(void);
void Node_remove(void);
void Node_kill(void);
void Node_alive(void);
void Node_groups(void);



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
        Decal_delete(self->decal);
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

#ifdef __NODE_MAIN__
int main() { return 0; }
#endif
#endif

