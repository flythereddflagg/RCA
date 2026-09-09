#ifndef __VALARRAY_C__
#define __VALARRAY_C__
#ifndef __MAIN__
#define __MAIN__
#define __VALARRAY_MAIN__
#endif

#include "core.h"
#include "dict.c"
#include "lstring.c"
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#define VALARRAYKEYLENGTH 256
#define VALARRAYSIZE 256
#define HASHPRIME 31
#define NO_NEXT -1

struct ValArrayData {
    int length;
    DynValue *vals;
    DynType *types;
};

ValArray ValArray_new() {
    // check(length > 0, "invalid length supplied");
    ValArray arr = (ValArray)malloc(sizeof(struct ValArrayData) * VALARRAYSIZE);
    check_mem(arr);
    arr->length = 0;
    arr->vals = (DynValue *)malloc(sizeof(DynValue) * VALARRAYSIZE);
    arr->types = (DynType *)malloc(sizeof(DynType) * VALARRAYSIZE);
    check_mem(arr->vals);
    check_mem(arr->types);
    for (int i = 0; i < arr->length; i++) {
        arr->vals[i] = EMPTYVAL;
        arr->types[i] = NONE;
    }
error:
    return arr;
}
ValArray ValArray_delete(ValArray arr) {
    if (arr) {
        for (int i = 0; i < arr->length; i++) {
            if (arr->types[i] == DICT)
                Dict_delete(arr->vals[i]._dict_);
            else if (arr->types[i] == ARR)
                ValArray_delete(arr->vals[i]._arr_);
            else if (arr->types[i] == STR)
                Lstring_delete(arr->vals[i]._str_);
        }
        if (arr->vals) {
            free(arr->vals);
            arr->vals = NULL;
        }
        if (arr->types) {
            free(arr->types);
            arr->types = NULL;
        }
        arr->length = 0;
        free(arr);
        arr = NULL;
    }
    return arr;
}
DynValue ValArray_get_at(ValArray arr, int index) {
    // allows negative indexing
    check(arr, "array is NULL");
    index = index < 0 ? arr->length + index % arr->length : index;
    check(index < arr->length, "index %d out of bounds for length %d", index,
          arr->length);
    return arr->vals[index];
error:
    return EMPTYVAL;
}

DynType ValArray_type_at(ValArray arr, int index) {
    // allows negative indexing
    check(arr, "array is NULL");
    index = index < 0 ? arr->length + index % arr->length : index;
    check(index < arr->length, "index %d out of bounds for length %d", index,
          arr->length);
    return arr->types[index];
error:
    return NONE;
}

int ValArray_set_at(ValArray arr, int index, DynType type, DynValue val) {
    check(arr, "array is NULL");
    index = index < 0 ? arr->length + index % arr->length : index;
    check(index < arr->length, "index %d out of bounds for length %d", index,
          arr->length);
    arr->vals[index] = val;
    arr->types[index] = type;
    return 0;
error:
    return -1;
}
int ValArray_append(ValArray arr, DynType type, DynValue val) {
    check(arr, "array is NULL");
    check(arr->length <= VALARRAYSIZE, "Array is full");
    arr->length += 1;
    return ValArray_set_at(arr, arr->length - 1, type, val);
error:
    return -1;
}

int ValArray_insert(ValArray arr, int index, DynType type, DynValue val) {
    check(arr, "array is NULL");
    index = index < 0 ? arr->length + index % arr->length : index;
    check(!ValArray_append(arr, NONE, EMPTYVAL), "insertion failed at append");
    for (int i = arr->length - 1; i > index; i--) {
        arr->types[i] = arr->types[i - 1];
        arr->vals[i] = arr->vals[i - 1];
    }
    check(!ValArray_set_at(arr, index, type, val),
          "insertion failed at set_at");
    return 0;
error:
    return -1;
}
DynValue ValArray_remove(ValArray arr, int index) {
    check(arr, "array is NULL");
    index = index < 0 ? arr->length + index % arr->length : index;
    DynValue val = ValArray_get_at(arr, index);
    for (int i = index; i < arr->length - 1; i++) {
        arr->types[i] = arr->types[i + 1];
        arr->vals[i] = arr->vals[i + 1];
    }
    return val;
error:
    return EMPTYVAL;
}
bool ValArray_string_in(ValArray arr, char *cstring) {
    check(arr, "array is NULL");
    for (int i = 0; i < arr->length; i++) {
        if (STR != ValArray_type_at(arr, i))
            continue;
        if (Lstring_cstring_equal(ValArray_get_at(arr, i)._str_.cstring,
                                  cstring))
            return true;
    }
error:
    return false;
}

int ValArray_extend(ValArray arr1, ValArray arr2) {
    check(arr1 && arr2, "one of the given arrays is NULL");
    for (int i = 0; i < arr2->length; i++) {
        check(-1 != ValArray_append(arr1, arr2->types[i], arr2->vals[i]),
              "Error while trying to append arrays");
    }
    return 0;
error:
    return -1;
}
void ValArray_print(ValArray arr) {
    printf("{  ");

    for (int i = 0; i < arr->length; i++) {
        switch (arr->types[i]) {
        case NONE:
            printf("none");
            break;
        case DICT:
            Dict_print(arr->vals[i]._dict_);
            break;
        case ARR:
            ValArray_print(arr->vals[i]._arr_);
        case STR:
            printf("\"");
            Lstring_print(arr->vals[i]._str_);
            printf("\"");
            break;
        case INT:
            printf("%d", arr->vals[i]._int_);
            break;
        case FLOAT:
            printf("%f", arr->vals[i]._float_);
            break;
        case BOOL:
            printf("%s", arr->vals[i]._bool_ ? "true" : "false");
            break;
        case OBJ:
            printf("%p", arr->vals[i]._obj_);
            break;
        default:
            sentinel("invalid type") break;
        }
        printf(", ");
    }
    printf("\b\b }");
error:
    return;
}

#ifdef __VALARRAY_MAIN__
int test_arr() {
    int len = 10;
    ValArray arr = ValArray_new();
    ValArray_print(arr);
    for (int i = 0; i < len; i++) {
        ValArray_append(arr, INT, dynval(_int_, 0));
    }
    ValArray_insert(arr, 3, INT, dynval(_int_, 5));
    ValArray_append(arr, STR, dynval(_str_, Lstring_new("a string")));

    ValArray_print(arr);
    printf("\n");

    arr = ValArray_delete(arr);

    return 0;
}
int main() {
    log_info("compile successful");
    test_arr();
    return 0;
}
#endif
#endif
