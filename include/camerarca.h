#ifndef CAMERARCA_H
#define CAMERARCA_H
typedef struct CameraRCAData *CameraRCA;

#include "node.h"
#include "objlist.h"
#include "raylib.h"
#include "raymath.h"
#include "valarray.h"
#include <math.h>

struct CameraRCAData {
    ValArray mobile_groups;
    double cur_zoom;
    double slack;
    bool shaking;
    ObjList path;
};
int CameraRCA_setup(Node node);
int CameraRCA_update(Node node);
Node CameraRCA_delete(Node node);
int CameraRCA_pan(Node node, Vector2 vector);
int CameraRCA_screenshake(Node node, double length, double scale);
int CameraRCA_follow_player(Node node);
Vector2 CameraRCA_add_slack(Vector2 vector, double slack);
int CameraRCA_stop_at_border(Node node);
int CameraRCA_center_player(Node node);
int CameraRCA_zoom_by(Node node, double factor);
int CameraRCA_zoom_abs(Node node, double scale);
#endif
