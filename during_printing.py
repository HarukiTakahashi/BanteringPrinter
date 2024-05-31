import os, sys
import pygame
import random
import time
from printer import Printer
from scene_base import Scene

# 造形中のクラス
class DuringPrinting(Scene):
    
    def __init__(self, s):
        super().__init__(s)
        self.name = "DuringPrinting"
        self.gcode_file_name = ""

        self.image_button = None
        self.speed_up_amout = 20

    def set_image_button(self, img):
        self.image_button = img
    
    def draw(self):

        # 色の定義
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)
        # 画面設定
        width = self.screen.get_width()
        height = self.screen.get_height()

        # スピードプログレスバーの設定
        prg_speed_x_pos = width//2 - 100
        bar_speed_position = (prg_speed_x_pos, height//2-200)
        bar_speed_size = (500, 50)

        # プログレスバーの設定
        prg_x_pos = 50
        bar_position = (prg_x_pos, height-200)
        bar_size = (width-(prg_x_pos*2), 50)        


        font = pygame.font.Font(None, 80)
            
        self.screen.fill((255, 255, 255))
        rect = pygame.Rect(100, 100,width - 200, 400)
        color = (0, 0, 0)
        bg_color = (255, 255, 255)

        pygame.draw.rect(self.screen, bg_color, rect)
        text_surface = font.render("Now Printing!", True, color)
        self.screen.blit(text_surface, (width//2-100, 100))

        text_surface = font.render("   -> " + self.gcode_file_name, True, color)
        self.screen.blit(text_surface, (width//2-100, 160))

        text_surface = font.render("Let's cheer for the 3D printer", True, color)
        self.screen.blit(text_surface, (width//2+50, 500))
        text_surface = font.render("by hitting the button!!", True, color)
        self.screen.blit(text_surface, (width//2+50, 580))


        # スピードプログレスバー
        c = self.printer.feedrate
        m = 300
        font = pygame.font.Font(None, 64)
        t = "Printing Speed : " + str(c) + " / " + str(m)
        text_surface = font.render(t , True, color)
        self.screen.blit(text_surface, (bar_speed_position[0], bar_speed_position[1] - 60))

        pygame.draw.rect(self.screen, WHITE, (bar_speed_position[0], bar_speed_position[1], bar_speed_size[0], bar_speed_size[1]))
        pygame.draw.rect(self.screen, RED, (bar_speed_position[0], bar_speed_position[1], bar_speed_size[0] * (c / m), bar_speed_size[1]))
        pygame.draw.rect(self.screen, BLACK, (bar_speed_position[0], bar_speed_position[1], bar_speed_size[0], bar_speed_size[1]), 2)

        # プログレスバー
        c , m = self.printer.get_progress()
        font = pygame.font.Font(None, 64)
        t = "Progress : " + str(c) + " / " + str(m)
        text_surface = font.render(t , True, color)
        self.screen.blit(text_surface, (bar_position[0], bar_position[1] - 80))

        pygame.draw.rect(self.screen, WHITE, (bar_position[0], bar_position[1], bar_size[0], bar_size[1]))
        pygame.draw.rect(self.screen, GREEN, (bar_position[0], bar_position[1], bar_size[0] * (c / m), bar_size[1]))
        pygame.draw.rect(self.screen, BLACK, (bar_position[0], bar_position[1], bar_size[0], bar_size[1]), 2)


        # 画像表示
        #print(self.images[self.selected_index])
        img = self.images[self.selected_index]
        self.screen.blit(img, (150, height // 2 - img.get_height()+ 100 ))

        # ボタン画像
        self.image_button = pygame.transform.scale(self.image_button, (200, 200))
        self.screen.blit(self.image_button, (800, height // 2-100))

        # 温度の表示
        self.drawTemperature()
        pygame.display.flip()

    def is_printing(self):
        return self.printer.is_printing()

    def press(self):
        a = self.printer.feedrate + self.speed_up_amout
        if a > 500:
            a = 500
        self.printer.change_feedrate(a)
       
    def set_gcode_file_name(self, f):
        self.gcode_file_name = f
