#include <stdlib.h>
#include "dbg.h"

typedef struct NodeData* Node;

struct NodeData{
    void (*update)(const void* self);
    void (*delete)(void* self);
};

void Node_update(const void* self){
    // Node node = (Node) self;
    // statements...
    ;
}

void Node_delete(void* self){
    free(self);
}

Node Node_new(){
    Node self = (Node) malloc (sizeof(struct NodeData));
    check_mem(self);

    self->update = &Node_update;
    self->delete = &Node_delete;

error:
    return self;
}


