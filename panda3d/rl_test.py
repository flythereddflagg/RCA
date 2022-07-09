from pyray import *
init_window(800, 450, "Hello")
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    model = load_model("./boxes.obj")
    texture = load_texture("./texture.png")
    end_drawing()
close_window()