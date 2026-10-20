#ifndef __LSTRING_H__
#define __LSTRING_H__

Lstring to_Lstring(char *cstring);
Lstring Lstring_delete(Lstring str);
Lstring Lstring_new(char *cstring);
Lstring Lstring_set(Lstring old, char *cstring);
void Lstring_print(Lstring str);
bool Lstring_equal(const Lstring str, const Lstring other);
bool Lstring_cstring_equal(char *str, char *other);

#endif
