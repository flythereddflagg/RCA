#ifndef CAMERA_H
#define CAMERA_H
typedef struct CameraData *Camera;

#include "node.h"
#include "objlist.h"
#include "raylib.h"
#include "valarray.h"

struct CameraData {
    void *mobile_groups;
    double cur_zoom;
    double slack;
    bool shaking;
    ObjList path;
};
int Camera_setup(Node node);
int Camera_update(Node node);
Node Camera_delete(Node node);
int Camera_pan(Node node, Vector2 vector);
int Camera_screenshake(Node node, double length, double scale);
int Camera_follow_player(Node node);
int Camera_add_slack(Node node, Vector2 vector, double slack);
int Camera_stop_at_border(Node node);
int Camera_center_player(Node node);
int Camera_zoom_by(Node node, double factor);
int Camera_zoom_abs(Node node, double scale);
#endif
