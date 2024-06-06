import os, sys
import pygame
import random
import time
from printer import Printer
from scene_base import Scene

# 造形前のクラス
class PrintingResult(Scene):
    # アイテムを縦に並べるための数値
    item_height = 50
    item_margin = 10

    HOLD_TIME_MAX = 60

    
    def __init__(self, s):
        super().__init__(s)
        self.name = "PrintingResult"
        
    def draw(self):
        # 色の定義
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        BLACK = (0, 0, 0)
        PINK = (255,100,100)
        
        # 画面設定
        width = self.screen.get_width()
        height = self.screen.get_height()

        font = pygame.font.Font(None, 36)
            
        self.screen.fill((255, 255, 255))
        rect = pygame.Rect(100, 100,width - 200, 400)
        color = (0, 0, 0)
        bg_color = (255, 255, 255)

        font = pygame.font.Font(None, 64)
        text_surface = font.render("AAAA?", True, color)
        self.screen.blit(text_surface, (width//2-50, bar_position[1]+10))
        font = pygame.font.Font(None, 48)
        text_surface = font.render("(Hold the button)", True, color)
        self.screen.blit(text_surface, (width//2-125, bar_position[1]+50))
        # pygame.draw.rect(self.screen, bg_color, rect)

        self.drawTemperature()
        self.drawUserInfo()
        pygame.display.flip()


    def press(self):
        pass

