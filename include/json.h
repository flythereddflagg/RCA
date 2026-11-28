#ifndef JSON_H
#define JSON_H
#include "raylib.h"
#include "dict.h"
#include "valarray.h"
#include <string.h>

DynValue Json_parse_file(char* filename);


#endif