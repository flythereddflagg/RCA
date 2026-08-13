#ifndef __LSTRING_C__
#define __LSTRING_C__
#ifndef __MAIN__
#define __MAIN__
#define __LSTRING_MAIN__
#endif
#include "dbg.h"
#include <stdlib.h>
#define MAX_LSTRING_LEN 500

typedef struct LStringData *LString;

struct LStringData {
    size_t length;
    char *cstring;
};

LString LString_delete(LString self) {
    check(self, "'self' is NULL");
    if (self->cstring)
        free(self->cstring);
    self->cstring = NULL;
    free(self);
error:
    return NULL;
}

LString LString_new(char *cstring) {
    LString self = (LString)malloc(sizeof(struct LStringData));
    check_mem(self);
    check(cstring, "invalid string supplied");
    self->length = strnlen(cstring, MAX_LSTRING_LEN);
    self->cstring = (char *)malloc(sizeof(char) * (self->length + 1));
    check_mem(self->cstring) strncpy(self->cstring, cstring, MAX_LSTRING_LEN);
    // guarentee all LStrings are null terminated upon creation
    self->cstring[length] = '\0';
error:
    return self;
}

int LString_print(LString self) { return 0; }

int LString_equal(LString self, )

#endif
#ifdef __LSTRING_MAIN__
int main() { return 0; }
#endif
