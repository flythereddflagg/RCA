#ifndef __OBJLIST_H__
#define __OBJLIST_H__

typedef struct LnodeData *Lnode;
typedef struct ObjListData *ObjList;

ObjList ObjList_new();
int ObjList_push(ObjList list, void *obj);
void *ObjList_pop(ObjList list);
ObjList ObjList_delete(ObjList list);
void *ObjList_at(ObjList list, size_t index);
void *ObjList_set_at(ObjList list, size_t index, void *obj);
int ObjList_insert(ObjList list, size_t index, void *obj);
void *ObjList_remove_at(ObjList list, size_t index);
void *ObjList_remove(ObjList list, void *obj);
bool ObjList_has(ObjList list, void *obj);
int ObjList_extend(ObjList list1, ObjList list2);

#endif
