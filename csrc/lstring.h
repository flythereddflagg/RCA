#ifndef __LSTRING_H__
#define __LSTRING_H__
#include <stdbool.h>
#define MAX_LSTRING_LEN 1024
#define Lstring_format(str) (int)str.length, str.cstring
#define LSTRING_NULL                                                           \
    (Lstring) { .length = 0, .cstring = NULL, .on_heap = false }
#define LSTRING_FMT "%.*s"
typedef struct LstringData Lstring;
struct LstringData {
    size_t length;
    char *cstring;
    bool on_heap;
};
Lstring to_Lstring(char *cstring);
Lstring Lstring_delete(Lstring str);
Lstring Lstring_new(char *cstring);
Lstring Lstring_set(Lstring old, char *cstring);
void Lstring_print(Lstring str);
bool Lstring_equal(const Lstring str, const Lstring other);
bool Lstring_cstring_equal(char *str, char *other);

#endif
