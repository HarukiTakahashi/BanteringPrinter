import os, sys
import pygame
import random
import time
from printer import Printer
from scene_base import Scene

# 造形前のクラス
class AfterPrinting(Scene):
    # アイテムを縦に並べるための数値
    item_height = 50
    item_margin = 10

    
    def __init__(self, s):
        super().__init__(s)
        self.name = "AfterPrinting"
    
    def set_printer(self,p):
        self.printer = p
    
    def draw(self):
        
        # 画面設定
        width = self.screen.get_width()
        height = self.screen.get_height()
        font = pygame.font.Font(None, 36)
            
        self.screen.fill((255, 255, 255))
        rect = pygame.Rect(100, 100,width - 200, 400)
        color = (0, 0, 0)
        bg_color = (255, 255, 255)
            
        pygame.draw.rect(self.screen, bg_color, rect)
        text_surface = font.render("Evaluate the outcome?", True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

        self.drawTemperature()
        pygame.display.flip()

    def press(self):
        print("thx")    
