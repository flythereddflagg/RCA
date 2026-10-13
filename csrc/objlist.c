#ifndef __OBJLIST_C__
#define __OBJLIST_C__
#ifndef __MAIN__
#define __MAIN__
#define __OBJLIST_MAIN__
#endif
#include "core.h"
#include <stdlib.h>

typedef struct LnodeData *Lnode;
typedef struct ObjListData *ObjList;
struct LnodeData {
    void *obj;
    Lnode next;
};
struct ObjListData {
    size_t length;
    Lnode head;
    Lnode tail;
};

ObjList ObjList_new() {
    ObjList list = (ObjList)malloc(sizeof(struct ObjListData));
    check_mem(list);
    list->length = 0;
    list->head = NULL;
    list->tail = NULL;
error:
    return list;
}
int ObjList_push(ObjList list, void *obj) {
    check(list, "list is NULL");
    Lnode new_node = (Lnode)malloc(sizeof(struct LnodeData));
    check_mem(new_node);
    new_node->obj = obj;
    new_node->next = NULL;
    if (!list->head && !list->tail) {
        // case for an empty list
        list->head = new_node;
        list->tail = new_node;
        list->length++;
        return 0;
    }
    check(list->head, "list->head is NULL!");
    check(list->tail, "list->tail is NULL!");
    check(!list->tail->next, "list->tail->next is NOT NULL");
    list->tail->next = new_node;
    list->tail = new_node;
    list->length++;
    return 0;
error:
    return -1;
}
void *ObjList_pop(ObjList list) {
    void *out = NULL;
    check(list, "list is NULL");
    check(list->length, "list is empty");
    check(list->head && list->tail, "List data corruption detected");
    size_t i = 0;
    Lnode current = list->head;
    Lnode previous = NULL;
    while (current->next) {
        check(current, "current is NULL at postition %lu", i);
        previous = current;
        current = current->next;
        i++;
    }
    check(current == list->tail, "current->next is NOT tail");
    check(!current->next, "current->next is NOT NULL");
    if (previous) {
        previous->next = current->next;
        list->tail = previous;
    } else {
        // case where there is only one element in the list
        list->head = NULL;
        list->tail = NULL;
    }
    out = current->obj;
    free(current);
    list->length--;
    return out;
error:
    return NULL;
}
ObjList ObjList_delete(ObjList list) {
    check(list, "list is NULL");
    size_t len = list->length;
    for (size_t i = 0; i < len; i++) {
        ObjList_pop(list);
    }
    free(list);
error:
    return NULL;
}
void *ObjList_at(ObjList list, size_t index) {
    check(list, "list is NULL");
    check(index < list->length, "index %lu out of bounds for length %lu", index,
          list->length);
    Lnode current = list->head;
    check(current, "head of list is NULL");
    for (size_t i = 0; i < index; i++) {
        current = current->next;
        check(current, "reached end of list (NULL) at position %lu", i);
    }
    return current->obj;
error:
    return NULL;
}

void *ObjList_set_at(ObjList list, size_t index, void *obj) {
    check(list, "list is NULL");
    check(index < list->length, "index %lu out of bounds for length %lu", index,
          list->length);
    Lnode current = list->head;
    check(current, "head of list is NULL");
    for (size_t i = 0; i < index; i++) {
        current = current->next;
        check(current, "reached end of list (NULL) at position %lu", i);
    }
    void *old_obj = current->obj;
    current->obj = obj;
    return old_obj;
error:
    return NULL;
}

int ObjList_insert(ObjList list, size_t index, void *obj) {
    check(list, "list is NULL");
    if (index == list->length)
        return ObjList_push(list, obj);
    check(index < list->length, "index %lu out of bounds for length %lu", index,
          list->length);
    check(list->head && list->tail, "List data corruption detected");
    Lnode new_node = (Lnode)malloc(sizeof(struct LnodeData));
    check_mem(new_node);
    new_node->obj = obj;
    new_node->next = NULL;
    Lnode current = list->head;
    Lnode previous = NULL;
    for (size_t i = 0; i < index; i++) {
        check(current, "current is NULL at postition %lu", i);
        previous = current;
        current = current->next;
    }
    if (previous) {
        new_node->next = current;
        previous->next = new_node;
    } else {
        // case where insert is at 0
        new_node->next = list->head;
        list->head = new_node;
    }
    list->length++;
    return 0;
error:
    return -1;
}
void *ObjList_remove_at(ObjList list, size_t index) {
    void *out = NULL;
    check(list, "list is NULL");
    if (index == list->length - 1)
        return ObjList_pop(list);
    check(index < list->length - 1, "index %lu out of bounds for length %lu",
          index, list->length);
    check(list->head && list->tail, "List data corruption detected");
    Lnode current = list->head;
    Lnode previous = NULL;
    for (size_t i = 0; i < index; i++) {
        check(current, "current is NULL at postition %lu", i);
        previous = current;
        current = current->next;
    }
    if (previous) {
        previous->next = current->next;
    } else {
        // case where remove is at 0
        list->head = current->next;
    }
    out = current->obj;
    free(current);
    list->length--;
    return out;
error:
    return NULL;
}
void *ObjList_remove(ObjList list, void *obj) {
    // remove by value of obj
    check(list, "list is NULL");
    Lnode current = list->head;
    void *matched_obj = NULL;
    for (size_t i = 0; i < list->length; i++) {
        check(current, "current is NULL at postition %lu", i);
        if (current->obj == obj) {
            matched_obj = ObjList_remove_at(list, i);
            return matched_obj;
        }
        current = current->next;
    }
    sentinel("object not found in list");
error:
    return NULL;
}
bool ObjList_has(ObjList list, void *obj) {
    check(list, "list is NULL");
    Lnode current = list->head;
    for (size_t i = 0; i < list->length; i++) {
        check(current, "current is NULL at postition %lu", i);
        if (current->obj == obj)
            return true;
        current = current->next;
    }
error:
    return false;
}
int ObjList_extend(ObjList list1, ObjList list2) {
    check(list1, "list 1 is null");
    check(list2, "list 2 is null");
    for (size_t i = 0; i < list2->length; i++) {
        check(!ObjList_push(list1, ObjList_at(list2, i)),
              "list2 obj push failed at index %lu", i);
    }
    return 0;
error:
    return -1;
}

#ifdef __OBJLIST_MAIN__
int main() {
    ObjList list = ObjList_new();
    ObjList_push(list, "cheese");
    char *cheese = (char *)ObjList_pop(list);
    debug("%s", cheese);
    ObjList_push(list, "cheese!");
    ObjList_push(list, "crackers");
    ObjList_push(list, "sausage");
    ObjList_push(list, "naan");
    ObjList_push(list, "charcuterie");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list, i));
    }
    debug("\n\n-- getting and setting --\n");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_set_at(list, i, "peas"));
    }
    debug("\n\n-- after setting --\n");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list, i));
    }
    ObjList_insert(list, 0, "cheese! 0");
    ObjList_insert(list, 3, "cheese! 3");
    ObjList_insert(list, 2, "cheese! 2");
    ObjList_insert(list, 0, "cheese! 00");
    ObjList_insert(list, 2, "cheese! 2");
    ObjList_insert(list, list->length, "cheese! end");
    debug("\n\n-- after inserting --\n");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list, i));
    }
    debug("\n\n-- removing --\n");

    debug("at %lu got '%s'", (size_t)2, (char *)ObjList_remove_at(list, 2));
    debug("at %lu got '%s'", (size_t)0, (char *)ObjList_remove_at(list, 0));
    debug("at %lu got '%s'", (size_t)5, (char *)ObjList_remove_at(list, 5));
    debug("at %lu got '%s'", (size_t)3, (char *)ObjList_remove_at(list, 3));
    debug("at %lu got '%s'", (size_t)2, (char *)ObjList_remove_at(list, 2));
    debug("at %lu got '%s'", list->length - 1,
          (char *)ObjList_remove_at(list, list->length - 1));
    debug("\n\n-- after removing --\n");
    for (size_t i = 0; i < list->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list, i));
    }
    debug("\n\n-- has? --\n");
    debug("list has '%s'? %s", (char *)ObjList_at(list, 3),
          ObjList_has(list, ObjList_at(list, 3)) ? "true" : "false");
    debug("list has '%s'? %s", "not cheese",
          ObjList_has(list, "not cheese") ? "true" : "false");
    debug("\n\n-- concat --\n");
    ObjList list2 = ObjList_new();
    ObjList_extend(list2, list);
    for (size_t i = 0; i < list2->length; i++) {
        debug("at %lu got '%s'", i, (char *)ObjList_at(list2, i));
    }
    ObjList_delete(list);
    ObjList_delete(list2);
    return 0;
}
#endif
#endif
