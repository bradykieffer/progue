import os
from lib import libtcodpy as libtcod
from utils.render_utils import SCREEN_HEIGHT, SCREEN_WIDTH
from engine import GameEngine


class Client(object):

    def __init__(self):
        self.font_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'assets/terminal12x12_gs_ro.png')
        libtcod.console_set_custom_font(
            self.font_path, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        self.engine = GameEngine(title='progue')

    def run(self):
        self.engine.init()
        while not libtcod.console_is_window_closed():
            exit = self.engine.update()
            if exit:
                break
