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
#define Lstring_format(self) (int)self.length, self.cstring
#define LSTRING_NULL                                                           \
    (Lstring) { .length = 0, .cstring = NULL }

Lstring to_Lstring(char *cstring) {
    // return an Lstring without copying and allocating new memory.
    // This can be risky.
    return (Lstring){.length = strnlen(cstring, MAX_LSTRING_LEN),
                     .cstring = cstring};
}

Lstring Lstring_delete(Lstring self) {
    if (self.cstring)
        free(self.cstring);
    return LSTRING_NULL;
}

Lstring Lstring_new(char *cstring) {
    // Lstring self = (Lstring)malloc(sizeof(struct LstringData));
    // check_mem(self);
    check(cstring, "invalid string supplied");
    Lstring self = {.length = strnlen(cstring, MAX_LSTRING_LEN),
                    .cstring =
                        (char *)malloc(sizeof(char) * (self.length + 1))};
    // self.length = strnlen(cstring, MAX_LSTRING_LEN);
    check(self.length < MAX_LSTRING_LEN, "invalid C string supplied");
    // self.cstring = (char *)malloc(sizeof(char) * (self.length + 1));
    check_mem(self.cstring);
    strncpy(self.cstring, cstring, self.length + 1);
    // guarentee all Lstrings are null terminated upon creation
    self.cstring[self.length] = '\0';
error:
    return self;
}
Lstring Lstring_set(Lstring old, char *cstring) {
    Lstring_delete(old);
    return Lstring_new(cstring);
}

void Lstring_print(Lstring self) { printf(LSTRING_FMT, Lstring_format(self)); }

bool Lstring_equal(const Lstring self, const Lstring other) {
    if (self.cstring && other.cstring && self.length == other.length &&
        !strncmp(self.cstring, other.cstring, self.length))

        return true;
    return false;
}

bool Lstring_cstring_equal(char *self, char *other) {
    Lstring s = Lstring_new(self), o = Lstring_new(other);
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
