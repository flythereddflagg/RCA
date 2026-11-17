#include "camera.h"

int Camera_setup(Node node) {
    check(node, "Node is NULL");
    check(Lstring_equal(node->type, to_Lstring("Camera")),
          "Node->type is '" LSTRING_FMT "', not Camera",
          Lstring_format(node->type));
    node->update = Camera_update;
    node->delete = Camera_delete;
    node->attr = (Camera)malloc(sizeof(struct CameraData));
    check_mem(node->attr);
    Camera camera = (Camera)node->attr;
    camera->mobile_groups = ValArray_new();
    Valarray draw_layers = node->scene->draw_layers;

    for (int i = 0; i < draw_layers->length; i++) {
        if (ValArray_type_at(draw_layers, i) == STR &&
            Lstring_equal(ValArray_get_at(draw_layers, i)._str_,
                          to_Lstring("hud"))) {
            continue;
        }
        ValArray_append(camera->mobile_groups, ValArray_get_at(draw_layers, i));
    }
    
}
int Camera_update(Node node);
Node Camera_delete(Node node) {
    check(node, "node is NULL");

    Camera camera = (Camera)node->attr;
    int n_layers = camera->mobile_groups;
    for (int i = 0; i < n_layers; i++) {
        // this valarray owns none of its elements
        ValArray_remove(camera->mobile_groups, -1);
    }
    camera->mobile_groups = Valarray_delete(camera->mobile_groups);
    if (node->attr) {
        free(node->attr);
        node->attr = NULL;
    }
    node = Node_delete(node);
error:
    return NULL;
}
int Camera_pan(Node node, Vector2 vector);
int Camera_screenshake(Node node, double length, double scale);
int Camera_follow_player(Node node);
int Camera_add_slack(Node node, Vector2 vector, double slack);
int Camera_stop_at_border(Node node);
int Camera_center_player(Node node);
int Camera_zoom_by(Node node, double factor);
int Camera_zoom_abs(Node node, double scale);
