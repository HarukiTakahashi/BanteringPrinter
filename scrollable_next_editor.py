import os, sys
import pygame
import random
import time
from scrollable import Scrollable


# class for making a scollable object
# this class is supposed to be inherited
class NextEditor(Scrollable):

    def __init__(self, screen, pos_start:tuple,pos_end:tuple, size=(100,100)):
        super().__init__(screen, pos_start,pos_end,size)


    def draw(self):
        text = "NEXT"
        font = pygame.font.Font(self.font_style, 58)
        line_spacing = 60
        BLACK = (0,0,0)
        WHITE=(255,255,255)
        LIGHT_YELLOW = (255,255,100)
    
        pygame.draw.rect(self.screen, LIGHT_YELLOW, [self.pos_x , self.pos_y, self.size[0],self.size[1]], 0)  # 線の太さ0は塗りつぶし
        pygame.draw.rect(self.screen, BLACK, [self.pos_x , self.pos_y, self.size[0],self.size[1]], 5)  # 線の太さ0は塗りつぶし

        pygame.draw.rect(self.screen, LIGHT_YELLOW, [self.pos_x-70,self.pos_y,70,len(text) * line_spacing], 0)  # inflateで少し余白を追加

        for i, char in enumerate(text):
            text_surface = font.render(char, True, BLACK)  # 文字を描画
            text_rect = text_surface.get_rect(topleft=(self.pos_x-60, self.pos_y + i * line_spacing))  # 各文字の位置
            self.screen.blit(text_surface, text_rect)  # 描画



