#ifndef __YAML_PARSE_H__
#define __YAML_PARSE_H__

typedef enum { YAML_NO_STATE, YAML_MAP_STATE, YAML_SEQ_STATE } yaml_state_t;
typedef struct {
    DynValue value;
    DynType type;
} DynTypeVal;

DynTypeVal YamlParse_parse_value(yaml_event_t event);
DynValue YamlParse_process_yaml_file(const char *filename);
int test_dict();
int test_init();

#endif
