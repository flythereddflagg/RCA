from src.tools import load_yaml
from src.input import Input 
import pygame as pg

pg.init()
game = load_yaml("./assets/__init__.yaml")
input_obj = Input(game)
while "QUIT" not in input_obj.get():
    print(input_obj.get())
pg.quit()
