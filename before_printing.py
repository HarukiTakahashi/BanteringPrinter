import os, sys
import pygame
import random
import time
from printer import Printer
from scene_base import Scene

# 造形前のクラス
class BeforePrinting(Scene):
    # アイテムを縦に並べるための数値
    item_height = 50
    item_margin = 10

    
    def __init__(self, s):
        super().__init__(s)
        self.name = "BeforePrinting"
        self.items = []
        self.items_num = 0
         
        self.highlight_index = 0
        self.roulette_coutner = 0
    
    def set_items(self, items):
        self.items = items        
        self.items_num = len(items)
    
    def draw(self):
        if self.active:
            self.roulette_coutner += 1
            if self.roulette_coutner % 10 == 0:
                self.highlight_index = (self.highlight_index + 1) % self.items_num
        
        # 画面設定
        width = self.screen.get_width()
        height = self.screen.get_height()
        font = pygame.font.Font(None, 36)
            
        self.screen.fill((255, 255, 255))
        for i, item in enumerate(self.items):
            rect = pygame.Rect(100, BeforePrinting.item_margin + i * BeforePrinting.item_height, 
                               width - 200, BeforePrinting.item_height - BeforePrinting.item_margin)
            color = (0, 0, 0)
            bg_color = (255, 255, 255)
            if self.highlight_index is not None and i == self.highlight_index:
                bg_color = (173, 216, 230)  # ライトブルーの背景色
                
            pygame.draw.rect(self.screen, bg_color, rect)
            text_surface = font.render(item, True, color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
        
        self.drawTemperature()
        pygame.display.flip()
        
    def stop(self):
        self.active = False
        print(self.items[self.highlight_index])
        
    def get_file(self):
        return self.items[self.highlight_index]