#include "camerarca.h"

int CameraRCA_setup(Node node) {
    check(node, "Node is NULL");
    check(Lstring_equal(node->type, to_Lstring("Camera")),
          "Node->type is '" LSTRING_FMT "', not Camera",
          Lstring_format(node->type));
    node->update = CameraRCA_update;
    node->delete = CameraRCA_delete;
    node->attr = (CameraRCA)malloc(sizeof(struct CameraRCAData));
    check_mem(node->attr);
    CameraRCA camera = (CameraRCA)node->attr;
    camera->mobile_groups = ValArray_new();
    ValArray draw_layers = node->scene->draw_layers;

    for (int i = 0; i < draw_layers->length; i++) {
        if (ValArray_type_at(draw_layers, i) == STR &&
            Lstring_equal(ValArray_get_at(draw_layers, i)._str_,
                          to_Lstring("hud"))) {
            continue;
        }
        ValArray_append(camera->mobile_groups, ValArray_type_at(draw_layers, i),
                        ValArray_get_at(draw_layers, i));
    }
    return 0;
error:
    return -1;
}
int CameraRCA_update(Node node) {
    check(node, "node is NULL");

    return 0;
error:
    return -1;
}
Node CameraRCA_delete(Node node) {
    check(node, "node is NULL");

    CameraRCA camera = (CameraRCA)node->attr;
    if (camera->mobile_groups) {
        int n_layers = camera->mobile_groups->length;
        for (int i = 0; i < n_layers; i++) {
            // this valarray owns none of its elements
            ValArray_remove(camera->mobile_groups, -1);
        }
        camera->mobile_groups = ValArray_delete(camera->mobile_groups);
    }
    if (node->attr) {
        free(node->attr);
        node->attr = NULL;
    }
    node = Node_delete(node);
error:
    return NULL;
}
int CameraRCA_pan(Node node, Vector2 vector);
int CameraRCA_screenshake(Node node, double length, double scale);
int CameraRCA_follow_player(Node node);
int CameraRCA_add_slack(Node node, Vector2 vector, double slack);
int CameraRCA_stop_at_border(Node node);
int CameraRCA_center_player(Node node);
int CameraRCA_zoom_by(Node node, double factor);
int CameraRCA_zoom_abs(Node node, double scale);
