#include "json.h"


DynValue Json_parse_file(char* filename){
    DynValue out_ref = EMPTYVAL;
    char * text = LoadFileText(filename);
    check(text, "text could not load");
    size_t text_len = strlen(text);
    char cur = '\0';
    for (size_t i = 0; i < text_len; i++){
        printf(" %c", text[i]);
    }
error:
    UnloadFileText(text);
    return out_ref;
}