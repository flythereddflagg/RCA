#ifndef __LSTRING_C__
#define __LSTRING_C__
#ifndef __MAIN__
#define __MAIN__
#define __LSTRING_MAIN__
#endif
#include "core.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#define MAX_LSTRING_LEN 1024
#define LSTRING_FMT "%.*s"
#define Lstring_format(str) (int)str.length, str.cstring
#define LSTRING_NULL                                                           \
    (Lstring) { .length = 0, .cstring = NULL, .on_heap = false }

Lstring to_Lstring(char *cstring) {
    // return an Lstring without copying and allocating new memory.
    // This can be risky.
    return (Lstring){.length = strnlen(cstring, MAX_LSTRING_LEN),
                     .cstring = cstring,
                     .on_heap = false};
}

Lstring Lstring_delete(Lstring str) {
    if (str.cstring && str.on_heap)
        free(str.cstring);
    return LSTRING_NULL;
}

Lstring Lstring_new(char *cstring) {
    check(cstring, "invalid string supplied");
    Lstring str = {.length = strnlen(cstring, MAX_LSTRING_LEN),
                   .cstring = (char *)malloc(sizeof(char) * (str.length + 1)),
                   .on_heap = true};
    check(str.length < MAX_LSTRING_LEN, "invalid C string supplied");
    check_mem(str.cstring);
    strncpy(str.cstring, cstring, str.length + 1);
    // guarentee all Lstrings are null terminated upon creation
    str.cstring[str.length] = '\0';
error:
    return str;
}
Lstring Lstring_set(Lstring old, char *cstring) {
    Lstring_delete(old);
    return Lstring_new(cstring);
}

void Lstring_print(Lstring str) { printf(LSTRING_FMT, Lstring_format(str)); }

bool Lstring_equal(const Lstring str, const Lstring other) {
    if (str.cstring && other.cstring && str.length == other.length &&
        !strncmp(str.cstring, other.cstring, str.length))

        return true;
    return false;
}

bool Lstring_cstring_equal(char *str, char *other) {
    Lstring s = Lstring_new(str), o = Lstring_new(other);
    bool equal = Lstring_equal(s, o);
    s = Lstring_delete(s);
    o = Lstring_delete(o);
    return equal;
}

#endif
#ifdef __LSTRING_MAIN__
int main() {
    Lstring str = Lstring_new("Its a string!");
    Lstring str2 = Lstring_new("Its a string?");
    log_info("equal? %d", Lstring_equal(str, str2));
    str2.cstring[str2.length - 1] = '!';
    log_info("how bout now? %d", Lstring_equal(str, str2));
    log_info("C string equal? %d", Lstring_cstring_equal("boy", "girl"));

    Lstring_print(str);
    printf("\n");
    str = Lstring_delete(str);
    str2 = Lstring_delete(str2);
    return 0;
}
#endif
