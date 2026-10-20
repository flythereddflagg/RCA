#ifndef __DICT_H__
#define __DICT_H__

int Dict_hash(const Lstring key);
int Dict_get_index(const Dict dict, const Lstring key);
int Dict_set(Dict dict, char *cstring, DynType type, DynValue val);
int Dict_delkey(Dict dict, char *cstring);
DynValue Dict_get(Dict dict, char *cstring, DynValue _default);
bool Dict_key_in(Dict dict, char *key);
void Dict_print(Dict dict);
void Dict_debug_print(Dict dict);
Dict Dict_new();
Dict Dict_copy(Dict dict);
Dict Dict_delete(Dict dict);
int test_dict();

#endif
