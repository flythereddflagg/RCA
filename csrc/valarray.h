#ifndef __VALARRAY_H__
#define __VALARRAY_H__

ValArray ValArray_new();
ValArray ValArray_delete(ValArray arr);
DynValue ValArray_get_at(ValArray arr, int index);
DynType ValArray_type_at(ValArray arr, int index);
int ValArray_set_at(ValArray arr, int index, DynType type, DynValue val);
int ValArray_append(ValArray arr, DynType type, DynValue val);
int ValArray_insert(ValArray arr, int index, DynType type, DynValue val);
DynValue ValArray_remove(ValArray arr, int index);
bool ValArray_has_string(ValArray arr, char *cstring);
int ValArray_extend(ValArray arr1, ValArray arr2);
void ValArray_print(ValArray arr);
ValArray ValArray_copy(ValArray arr);
int test_arr();

#endif
