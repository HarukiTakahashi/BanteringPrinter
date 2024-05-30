import os, sys
import pygame
import random
import time
from printer import Printer

# シーンの基底クラス
class Scene():
    
    def __init__(self, s):
        self.screen = s
        self.name = "base"
        self.active = False
        self.printer = None

        self.gcode_file = []
        self.images = []
    
    def draw(self):
        pass
        
    # プリンタのインスタンスを設定
    def set_printer(self, p: Printer):
        self.printer = p

    # 造形候補のGcodeファイル名と画像ファイル名を設定
    def set_gcode_file(self, g: list, img: list):
        self.gcode_file = list(g)
        self.images = list(img)

    # プリンタの温度について表示
    def drawTemperature(self):
        font = pygame.font.Font(None, 36)
        width = self.screen.get_width()
        height = self.screen.get_height()
        
        rect = pygame.Rect(100, height-200,200, height-100)

        text = "Nozzle temperature : " + str(self.printer.nozzle_temp) + " deg C"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, (100,height-100))

        text = "Bed temperature : " + str(self.printer.bed_temp) + " deg C"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, (100,height-50))

        text = "Speed : " + str(self.printer.feedrate) + "%"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, (600,height-100))