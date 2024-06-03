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

    HOLD_TIME_MAX = 180

    
    def __init__(self, s):
        super().__init__(s)
        self.name = "AfterPrinting"

        self.holdtime = 0
        
        
    def draw(self):
        
        # 画面設定
        width = self.screen.get_width()
        height = self.screen.get_height()
        img_margin = 100
        img_size = 500
        offset_y = -100
        font = pygame.font.Font(None, 36)
            
        self.screen.fill((255, 255, 255))
        rect = pygame.Rect(100, 100,width - 200, 400)
        color = (0, 0, 0)
        bg_color = (255, 255, 255)

        tw = width//2 - img_size // 2
        self.screen.blit(self.images[0], 
                         (tw - img_size - img_margin, height // 2- img_size // 2 + offset_y))
        self.screen.blit(self.images[1], 
                         (tw, height // 2- img_size // 2 + offset_y))
        self.screen.blit(self.images[2], 
                         (tw + img_size + img_margin, height // 2- img_size // 2 + offset_y)) 
        
        # プログレスバー   
        bar_size = (400, 100)
        bar_position = (width//2 - bar_size[0] // 2, height//2+200)
        font = pygame.font.Font(None, 64)
    

        # 色の定義
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 200, 200)
        BLACK = (0, 0, 0)

        pygame.draw.rect(self.screen, WHITE, 
                         (bar_position[0], bar_position[1], bar_size[0], bar_size[1]))
        pygame.draw.rect(self.screen, RED, 
                         (bar_position[0], bar_position[1], bar_size[0] * (self.holdtime / AfterPrinting.HOLD_TIME_MAX), bar_size[1]))
        pygame.draw.rect(self.screen, BLACK, 
                         (bar_position[0], bar_position[1], bar_size[0], bar_size[1]), 2)


        text_surface = font.render("OK?", True, color)
        self.screen.blit(text_surface, (width//2-50, bar_position[1]))
        # pygame.draw.rect(self.screen, bg_color, rect)
        text_surface = font.render("Evaluate the outcome?", True, color)
        self.screen.blit(text_surface, (width//2-50, height//2-300))

        self.drawTemperature()
        self.drawUserInfo()
        pygame.display.flip()


    def set_image(self, img: list):
        self.images = img


    def press(self):
        pass

    def hold_button(self):
        self.holdtime+=1

    def release_button(self):
        self.holdtime = 0
    
    def is_confirmed(self):
        print("ht"+str(self.holdtime))
        if self.holdtime > AfterPrinting.HOLD_TIME_MAX:
            return True
        else:
            return False
