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

    HOLD_TIME_MAX = 60

    
    def __init__(self, s):
        super().__init__(s)
        self.name = "AfterPrinting"

        self.holdtime = 0
        
        
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

        # 画像の位置設定
        img_margin = 100
        img_size = 500
        offset_y = -50
        img_position = (width//2 - img_size // 2, 
                        height // 2- img_size // 2 + offset_y)
        img_left_x = img_position[0] - img_size - img_margin
        img_right_x = img_position[0] + img_size + img_margin

        self.screen.blit(self.images[0], 
                         (img_left_x, img_position[1]))
        self.screen.blit(self.images[1], 
                         (img_position[0], img_position[1]))
        self.screen.blit(self.images[2], 
                         (img_right_x, img_position[1])) 
        
        font = pygame.font.Font(None, 64)
        
        if self.printer.nozzle_temp > 50:
            text_surface = font.render("[ Nozzle : " + str(self.printer.nozzle_temp) + " degC ]", True, RED)
        else:
            text_surface = font.render("[ Nozzle : " + str(self.printer.nozzle_temp) + " degC ]", True, BLUE)    
        self.screen.blit(text_surface, (img_left_x+100, img_position[1]-50))

        if self.printer.bed_temp > 40:
            text_surface = font.render("[ Bed : " + str(self.printer.bed_temp) + " degC ]", True, RED)
        else:
            text_surface = font.render("[ Bed : " + str(self.printer.bed_temp) + " degC ]", True, BLUE)    
        self.screen.blit(text_surface, (img_left_x+100, img_position[1] + img_size//2 + 120))

        font = pygame.font.Font(None, 36)
        text_surface = font.render("Wait until the nozzle and bed cool down.", True, color)
        self.screen.blit(text_surface, (img_left_x, img_position[1] + img_size+30))
        
        #if self.printer.bed_temp > 40 or self.printer.nozzle_temp > 50:
        text_surface = font.render("Do not touch them at high temperatures!", True, RED)
        self.screen.blit(text_surface, (img_left_x, img_position[1] + img_size+70))


        # 真ん中のメッセージ
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Remove the printed result from the bed.", True, color)
        self.screen.blit(text_surface, (img_position[0], img_position[1] + img_size+30))

        # 右のメッセージ
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Make sure the bed is in the correct position", True, color)
        self.screen.blit(text_surface, (img_right_x, img_position[1] + img_size+30))
        text_surface = font.render("and there is nothing on it", True, color)
        self.screen.blit(text_surface, (img_right_x, img_position[1] + img_size+70))
        # プログレスバー   
        bar_size = (400, 100)
        bar_position = (width//2 - bar_size[0] // 2, height//2+300)
        font = pygame.font.Font(None, 64)
    
        pygame.draw.rect(self.screen, WHITE, 
                         (bar_position[0], bar_position[1], bar_size[0], bar_size[1]))
        pygame.draw.rect(self.screen, PINK, 
                         (bar_position[0], bar_position[1], bar_size[0] * (self.holdtime / AfterPrinting.HOLD_TIME_MAX), bar_size[1]))
        pygame.draw.rect(self.screen, BLACK, 
                         (bar_position[0], bar_position[1], bar_size[0], bar_size[1]), 2)



        font = pygame.font.Font(None, 64)
        text_surface = font.render("OK?", True, color)
        self.screen.blit(text_surface, (width//2-50, bar_position[1]+10))
        font = pygame.font.Font(None, 48)
        text_surface = font.render("(Hold the button)", True, color)
        self.screen.blit(text_surface, (width//2-125, bar_position[1]+50))
        # pygame.draw.rect(self.screen, bg_color, rect)
        #text_surface = font.render("Evaluate the outcome?", True, color)
        #self.screen.blit(text_surface, (width//2-50, height//2-300))

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
        if self.holdtime > AfterPrinting.HOLD_TIME_MAX:
            return True
        else:
            return False
