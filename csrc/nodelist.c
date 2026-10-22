#include "nodelist.h"
#include "dbg.h"
#include <string.h>

NodeFunc Node_get_setup(char *key) {
    check(key, "key is NULL");
    for (size_t i = 0; i < SETUP_FUNCS_LENGTH; i++) {
        if (!strncmp(key, SETUP_FUNCS[i].key, MAX_KEY_LEN)) {
            return SETUP_FUNCS[i].func;
        }
    }
    sentinel("Node type '%s' is not a known type!", key);
error:
    return NULL;
}
