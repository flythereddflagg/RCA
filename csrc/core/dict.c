

#include "dict.h"

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

int Dict_get_index(const Dict dict, const Lstring key) {
    // TODO reimplement this more simply
    check(dict, "invalid dict supplied");
    check(key.cstring && key.cstring[0], "invalid key '%s' supplied",
          key.cstring);
    int hash_i = Dict_hash(key), index = 0, i = 0;
    // debug("%d", hash_i);

    // if the key at that index is not empty follow the linked list to the end
    while (dict->next[hash_i] != NO_NEXT) {
        if (Lstring_equal(key, dict->keys[hash_i]))
            return hash_i;
        hash_i = dict->next[hash_i];
    }
    // debug("%d", hash_i);

    // now we have the end of the current hash list
    // so we increment by 1 until we either find an empty slot or the given key
    index = hash_i;

    for (i = 0; i < DICTSIZE; i++) {
        if (Lstring_equal(key, dict->keys[hash_i]) ||
            !dict->keys[index].cstring)
            break;
        index++;
        // wrap around
        if (index >= DICTSIZE)
            index = index % DICTSIZE;
    }
    check(i < DICTSIZE, "Dict is full");
    // then if we needed to find another slot, we link to it in the previous one
    if (hash_i != index)
        dict->next[hash_i] = index;

    check(index >= 0 && index < DICTSIZE, "invalid index '%d' detected", index);

    return index;
error:
    return -1;
}

int Dict_set(Dict dict, char *cstring, DynType type, DynValue val) {
    check(dict, "invalid dict supplied");
    check(cstring && cstring[0], "invalid key supplied: '%s'", cstring);
    Lstring key = Lstring_new(cstring);
    int index = Dict_get_index(dict, key);
    check(index >= 0 && index < DICTSIZE, "Index error '%d'", index);

    dict->keys[index] = Lstring_delete(dict->keys[index]);
    if (dict->types[index] == DICT)
        dict->vals[index]._dict_ = Dict_delete(dict->vals[index]._dict_);
    else if (dict->types[index] == ARR)
        dict->vals[index]._arr_ = ValArray_delete(dict->vals[index]._arr_);
    else if (dict->types[index] == STR)
        dict->vals[index]._str_ = Lstring_delete(dict->vals[index]._str_);
    // then put in the new one
    dict->keys[index] = key;
    dict->types[index] = type;
    dict->vals[index] = val;
    return 0;
error:
    return -1;
}

int Dict_delkey(Dict dict, char *cstring) {
    check(dict, "invalid dict supplied");
    check(cstring && cstring[0], "invalid key '%s' supplied", cstring);
    Lstring key = to_Lstring(cstring);
    int prev = Dict_hash(key), index = prev;
    // if keys do not match follow the linked list and error if we reach the end
    while (!dict->keys[index].cstring ||
           Lstring_equal(key, dict->keys[index])) {
        check(dict->next[index] != NO_NEXT, "'" LSTRING_FMT "' Key not found",
              Lstring_format(key));
        prev = index;
        index = dict->next[index];
    }

    // we now have the index which we erase saving the 'next' value
    int tmp_next = dict->next[index];
    dict->keys[index] = Lstring_delete(dict->keys[index]);
    dict->next[index] = NO_NEXT;
    // then we set the prev item to be the next
    dict->next[prev] = tmp_next;
    return 0;
error:
    return -1;
}

DynValue Dict_get(Dict dict, char *cstring, DynValue _default) {
    check(dict, "invalid dict supplied");
    check(cstring && cstring[0], "invalid key '%s' supplied", cstring);
    Lstring key = to_Lstring(cstring);
    int index = Dict_get_index(dict, key);
    check_debug(Lstring_equal(dict->keys[index], key),
                "key '" LSTRING_FMT "' not found!", Lstring_format(key));
    return dict->vals[index];

error:
    return _default;
}

bool Dict_key_in(Dict dict, char *key) {
    Lstring key_in = Lstring_new(key);
    check(dict, "dict is NULL");
    check(key, "key is NULL");
    for (int i = 0; i < DICTSIZE; i++) {
        if (Lstring_equal(key_in, dict->keys[i])) {
            key_in = Lstring_delete(key_in);
            return true;
        }
    }

error:
    key_in = Lstring_delete(key_in);
    return false;
}

void Dict_print(Dict dict) {
    check(dict, "NULL dict supplied");
    printf("{");

    for (int i = 0; i < DICTSIZE; i++) {
        if (!dict->keys[i].cstring || !dict->keys[i].cstring[0])
            continue;
        printf("\"%s\" : ", dict->keys[i].cstring);
        switch (dict->types[i]) {
        case NONE:
            printf("null");
            break;
        case DICT:
            Dict_print(dict->vals[i]._dict_);
            break;
        case ARR:
            ValArray_print(dict->vals[i]._arr_);
            break;
        case STR:
            printf("\"" LSTRING_FMT "\"", Lstring_format(dict->vals[i]._str_));
            break;
        case INT:
            printf("%d", dict->vals[i]._int_);
            break;
        case FLOAT:
            printf("%f", dict->vals[i]._float_);
            break;
        case BOOL:
            printf("%s", dict->vals[i]._bool_ ? "true" : "false");
            break;
        case OBJ:
            printf("%p", dict->vals[i]._obj_);
            break;
        default:
            sentinel("invalid type");
            break;
        }
        printf(", ");
    }
    printf("\b\b}");
error:
    return;
}

void Dict_debug_print(Dict dict) {
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

            printf("  str \"%-19.*s\"", Lstring_format(dict->vals[i]._str_));
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
ValArray ValArray_copy(ValArray arr);

Dict Dict_copy(Dict dict) {
    Dict copy = Dict_new();
    check(dict, "dict to copy is NULL");
    check(copy, "Dict copy failed.");
    char *key;
    DynValue val;
    for (int i = 0; i < DICTSIZE; i++) {
        if (!dict->keys[i].cstring || !dict->keys[i].cstring[0])
            continue;
        key = dict->keys[i].cstring;
        val = dict->vals[i];
        switch (dict->types[i]) {
        case NONE:
            Dict_set(copy, key, NONE, dynval(_obj_, NULL));
            break;
        case DICT:
            Dict_set(copy, key, DICT, dynval(_dict_, Dict_copy(val._dict_)));
            Dict_set(copy, key, ARR, dynval(_arr_, ValArray_copy(val._arr_)));
            break;
        case ARR:
            Dict_set(copy, key, ARR, dynval(_arr_, ValArray_copy(val._arr_)));
            break;
        case STR:
            Dict_set(copy, key, STR,
                     dynval(_str_, Lstring_new(val._str_.cstring)));
            break;
        case INT:
            Dict_set(copy, key, INT, val);
            break;
        case FLOAT:
            Dict_set(copy, key, FLOAT, val);
            break;
        case BOOL:
            Dict_set(copy, key, BOOL, val);
            break;
        case OBJ:
            Dict_set(copy, key, OBJ, val);
            break;
        default:
            sentinel("invalid type") break;
        }
    }
error:
    return copy;
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

int main() {
    log_info("compile successful");
    test_dict();
    return 0;
}
#endif
