#ifndef __OBJLIST_C__
#define __OBJLIST_C__
#ifndef __MAIN__
#define __MAIN__
#define __OBJLIST_MAIN__
#endif
#include "core.h"

typedef struct LnodeData *Lnode;
typedef struct ObjListData *ObjList;
struct LnodeData {
    void *obj;
    Lnode next;
}
struct ObjListData {
    size_t length;
    Lnode head;
}

ObjList ObjList_new(){
    ObjList list = (ObjList) malloc(sizeof(struct ObjListData));
    check_mem(list);
    list->length = 0;
    list->head = NULL;
error:
    return list;
}
ObjList ObjList_delete();
void *ObjList_at(ObjList list, int index);
int ObjList_set_at(ObjList list, int index, void *obj);
int ObjList_append(ObjList list, void *obj);
int ObjList_insert(ObjList list, int index, void *obj);
void *ObjList_remove(ObjList list, int index);
bool ObjList_has(ObjList list, void *obj);
int ObjList_extend(ObjList list1, ObjList list2);

#ifdef __OBJLIST_MAIN__
int main() { return 0; }
#endif
#endif