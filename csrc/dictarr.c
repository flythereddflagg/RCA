#ifndef __DICTARR_C__
#define __DICTARR_C__
#ifndef __MAIN__
#define __MAIN__
#define __DICT_MAIN__
#endif

#include "core.h"
#include "lstring.c"
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#define DICTKEYLENGTH 256
#define DICTSIZE 256
#define HASHPRIME 31
#define NO_NEXT -1
#define EMPTYVAL                                                               \
    (DynValue) { ._obj_ = NULL }
#define dynval(T, V)                                                           \
    (DynValue) { .T = V }

void Dict_print(Dict dict);
Dict Dict_delete(Dict dict);
enum DynTypeData { NONE, DICT, ARR, STR, INT, FLOAT, BOOL, OBJ };

union DynValueData {
    Dict _dict_;
    ValArray _arr_;
    Lstring _str_;
    int _int_;
    float _float_;
    bool _bool_;
    void *_obj_;
    // NULL none;
};

struct ValArrayData {
    int length;
    DynValue *vals;
    DynType *types;
};

ValArray ValArray_new() {
    // check(length > 0, "invalid length supplied");
    ValArray arr = (ValArray)malloc(sizeof(struct ValArrayData) * DICTSIZE);
    check_mem(arr);
    arr->length = 0;
    arr->vals = (DynValue *)malloc(sizeof(DynValue) * DICTSIZE);
    arr->types = (DynType *)malloc(sizeof(DynType) * DICTSIZE);
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
    check(arr->length <= DICTSIZE, "Array is full");
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

// #####################################################################

struct DictData {
    Lstring *keys;
    DynType *types;
    DynValue *vals;
    int *next;
};

int Dict_hash(const Lstring key) {
    check(key.cstring && key.cstring[0], "invalid key to hash %s", key.cstring);
    char hash = 0;
    int i = 0;
    for (i = 0; i < key.length; i++) {
        hash = hash ^ key.cstring[i];
    }
    return (int)hash % DICTSIZE;
error:
    return -1;
}

int Dict_get_index(const Dict self, const Lstring key) {
    // TODO reimplement this more simply
    check(self, "invalid dict supplied");
    check(key.cstring && key.cstring[0], "invalid key '%s' supplied",
          key.cstring);
    int hash_i = Dict_hash(key), index = 0, i = 0;
    // debug("%d", hash_i);

    // if the key at that index is not empty follow the linked list to the end
    while (self->next[hash_i] != NO_NEXT) {
        if (Lstring_equal(key, self->keys[hash_i]))
            return hash_i;
        hash_i = self->next[hash_i];
    }
    // debug("%d", hash_i);

    // now we have the end of the current hash list
    // so we increment by 1 until we either find an empty slot or the given key
    index = hash_i;

    for (i = 0; i < DICTSIZE; i++) {
        if (Lstring_equal(key, self->keys[hash_i]) ||
            !self->keys[index].cstring)
            break;
        index++;
        // wrap around
        if (index >= DICTSIZE)
            index = index % DICTSIZE;
    }
    check(i < DICTSIZE, "Dict is full");
    // then if we needed to find another slot, we link to it in the previous one
    if (hash_i != index)
        self->next[hash_i] = index;

    check(index >= 0 && index < DICTSIZE, "invalid index '%d' detected", index);

    return index;
error:
    return -1;
}

int Dict_set(Dict self, char *cstring, DynType type, DynValue val) {
    check(self, "invalid dict supplied");
    check(cstring && cstring[0], "invalid key supplied: '%s'", cstring);
    Lstring key = Lstring_new(cstring);
    int index = Dict_get_index(self, key);
    check(index >= 0 && index < DICTSIZE, "Index error '%d'", index);

    self->keys[index] = Lstring_delete(self->keys[index]);
    if (self->types[index] == DICT)
        self->vals[index]._dict_ = Dict_delete(self->vals[index]._dict_);
    else if (self->types[index] == ARR)
        self->vals[index]._arr_ = ValArray_delete(self->vals[index]._arr_);
    else if (self->types[index] == STR)
        self->vals[index]._str_ = Lstring_delete(self->vals[index]._str_);
    // then put in the new one
    self->keys[index] = key;
    self->types[index] = type;
    self->vals[index] = val;
    return 0;
error:
    return -1;
}

int Dict_delkey(Dict self, char *cstring) {
    check(self, "invalid dict supplied");
    check(cstring && cstring[0], "invalid key '%s' supplied", cstring);
    Lstring key = to_Lstring(cstring);
    int prev = Dict_hash(key), index = prev;
    // if keys do not match follow the linked list and error if we reach the end
    while (!self->keys[index].cstring ||
           Lstring_equal(key, self->keys[index])) {
        check(self->next[index] != NO_NEXT, "'" LSTRING_FMT "' Key not found",
              Lstring_format(key));
        prev = index;
        index = self->next[index];
    }

    // we now have the index which we erase saving the 'next' value
    int tmp_next = self->next[index];
    self->keys[index] = Lstring_delete(self->keys[index]);
    self->next[index] = NO_NEXT;
    // then we set the prev item to be the next
    self->next[prev] = tmp_next;
    return 0;
error:
    return -1;
}

DynValue Dict_get(Dict self, char *cstring, DynValue _default) {
    check(self, "invalid dict supplied");
    check(cstring && cstring[0], "invalid key '%s' supplied", cstring);
    Lstring key = to_Lstring(cstring);
    int index = Dict_get_index(self, key);
    check(Lstring_equal(self->keys[index], key),
          "key '" LSTRING_FMT "' not found!", Lstring_format(key));
    return self->vals[index];

error:
    return _default;
}

void Dict_print(Dict dict) {
    check(dict, "NULL dict supplied");
    printf("{ ");
    printf("\n[ind]        key |  type                  val | next\n");
    printf("----------------------------------------------------\n");

    for (int i = 0; i < DICTSIZE; i++) {
        if (!dict->keys[i].cstring || !dict->keys[i].cstring[0])
            continue;
        printf("[%3d] %10s | ", i, dict->keys[i].cstring);
        switch (dict->types[i]) {
        case NONE:
            printf(" none %20s", "null");
            break;
        case DICT:
            printf(" dict ");
            Dict_print(dict->vals[i]._dict_);
            break;
        case ARR:
            printf("  arr ");
            ValArray_print(dict->vals[i]._arr_);
            break;
        case STR:
            // TODO fix padding
            /*
            The "%*.*s" can be placed before OR after your "%s", depending
            desire for LEFT or RIGHT padding.
            https://stackoverflow.com/questions/276827/string-padding-in-c
             */

            printf("  str \"%-19.*s", Lstring_format(dict->vals[i]._str_));
            break;
        case INT:
            printf("  int %20d", dict->vals[i]._int_);
            break;
        case FLOAT:
            printf("float %20f", dict->vals[i]._float_);
            break;
        case BOOL:
            printf(" bool %20s", dict->vals[i]._bool_ ? "true" : "false");
            break;
        case OBJ:
            printf("  obj %20p", dict->vals[i]._obj_);
            break;
        default:
            sentinel("invalid type") break;
        }
        if (dict->next[i] == NO_NEXT)
            printf(" | null\n");
        else
            printf(" | %d\n", dict->next[i]);
    }
    printf("\n}");
error:
    return;
}

Dict Dict_new() {
    Dict dict = (Dict)malloc(sizeof(struct DictData));
    check_mem(dict);
    dict->keys = (Lstring *)malloc(sizeof(Lstring) * DICTSIZE);
    check_mem(dict->keys);
    dict->types = (DynType *)malloc(sizeof(DynType) * DICTSIZE);
    check_mem(dict->types);
    dict->vals = (DynValue *)malloc(sizeof(DynValue) * DICTSIZE);
    check_mem(dict->vals);
    dict->next = (int *)malloc(sizeof(int) * DICTSIZE);
    check_mem(dict->next);

    for (int i = 0; i < DICTSIZE; i++) {
        dict->keys[i] = LSTRING_NULL;
        dict->types[i] = 0;
        dict->vals[i] = EMPTYVAL;
        dict->next[i] = NO_NEXT;
    }
    return dict;
error:
    return NULL;
}

Dict Dict_delete(Dict dict) {
    if (dict) {
        for (int i = 0; i < DICTSIZE; i++) {
            dict->keys[i] = Lstring_delete(dict->keys[i]);
            if (dict->types[i] == DICT)
                dict->vals[i]._dict_ = Dict_delete(dict->vals[i]._dict_);
            else if (dict->types[i] == ARR)
                dict->vals[i]._arr_ = ValArray_delete(dict->vals[i]._arr_);
            else if (dict->types[i] == STR)
                dict->vals[i]._str_ = Lstring_delete(dict->vals[i]._str_);
        }
        if (dict->keys)
            free(dict->keys);
        if (dict->types)
            free(dict->types);
        if (dict->vals)
            free(dict->vals);
        if (dict->next)
            free(dict->next);
        free(dict);
    }
    return NULL;
}

#endif
#ifdef __DICT_MAIN__
int test_dict() {
    log_info("compile successful");
    Dict dict = Dict_new();
    Dict_set(dict, "pickle", INT, dynval(_int_, 25));
    Dict_set(dict, "cheese", STR, dynval(_str_, Lstring_new("23")));
    Dict_set(dict, "crackers", STR,
             dynval(_str_, Lstring_new("holy guacamole")));
    Dict_set(dict, "crackers2", STR,
             dynval(_str_, Lstring_new("holy guacamole")));
    Dict_print(dict);
    Dict_delkey(dict, "pickle");
    Dict_print(dict);
    Dict_set(dict, "pickle", FLOAT, dynval(_float_, 26.2));
    Dict_print(dict);
    Dict_delkey(dict, "pickl");
    debug("getting value of pickle as %f",
          Dict_get(dict, "pickle", EMPTYVAL)._float_);
    Dict_set(dict, "cheese", OBJ, dynval(_obj_, dict));
    Dict_print(dict);
    Dict_delkey(dict, "pickle");
    Dict_delkey(dict, "cheese");
    Dict_delkey(dict, "crackers");
    Dict_print(dict);
    dict = Dict_delete(dict);
    return 0;
}

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
    test_dict();
    test_arr();
    return 0;
}
#endif
