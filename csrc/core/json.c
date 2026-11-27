#include "json.h"


DynVal Json_parse_file(char* filename){
    DynVal out_ref = EMPTYVAL;
    char * text = LoadFileText(filename);
    check(text, "text could not load");
    size_t text_len = strlen(text);
    for (size_t i = 0; i < text_len; i++){
        ; // continue here
    }
error:
    UnloadFileText(text);
    return out_ref;
}