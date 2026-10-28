#include "nodelist.h"
#include "decal.h"

KeyFuncPair SETUP_FUNCS[] = {
    kf_pair("Node", Node_setup),     kf_pair("Animation", Node_setup),
    kf_pair("Backpack", Node_setup), kf_pair("Cactus", Node_setup),
    kf_pair("Camera", Node_setup),   kf_pair("Coin", Node_setup),
    kf_pair("CutScene", Node_setup), kf_pair("Decal", Decal_setup),
    kf_pair("Edge", Node_setup),     kf_pair("Gate", Node_setup),
    kf_pair("Item", Node_setup),     kf_pair("Menu", Node_setup),
    kf_pair("Music", Node_setup),    kf_pair("OpenUrlTrigger", Node_setup),
    kf_pair("Retry", Node_setup),    kf_pair("SFX", Node_setup),
    kf_pair("SoftDirt", Node_setup), kf_pair("TextBox", Node_setup),
    kf_pair("TextRoll", Node_setup), kf_pair("Trigger", Node_setup)};

size_t SETUP_FUNCS_LENGTH = sizeof(SETUP_FUNCS) / sizeof(KeyFuncPair);
