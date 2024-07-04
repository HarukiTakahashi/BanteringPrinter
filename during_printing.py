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
        self.speed_up_amout = 10

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


        # プログレスバーの設定
        prg_x_pos = 100
        bar_position = (prg_x_pos, height-200)
        bar_size = (width-(prg_x_pos*2), 50)        


        #font = pygame.font.Font(None, 80)
            
        self.screen.fill((255, 255, 255))
        rect = pygame.Rect(100, 100,width - 200, 400)
        color = (0, 0, 0)
        bg_color = (255, 255, 255)

        pygame.draw.rect(self.screen, bg_color, rect)

        font = pygame.font.Font(self.font_style, 80)
        if self.printer.is_waiting:
            if self.lang == 0:
                text_surface = font.render("温度上昇中!", True, RED)
            elif self.lang == 1:
                text_surface = font.render("Now Heating!", True, RED)
        else:
            if self.lang == 0:
                text_surface = font.render("3Dプリント中!", True, color)
            elif self.lang == 1:
                text_surface = font.render("Now Printing!", True, color)
        self.screen.blit(text_surface, (750, 150))

        font = pygame.font.Font(self.font_style, 60)
        text_surface = font.render(" -> " + self.gcode_file_name, True, color)
        self.screen.blit(text_surface, (800, 250))


        cheer_pos_y = 400
        # ボタン画像
        self.image_button = pygame.transform.scale(self.image_button, (200, 200))
        self.screen.blit(self.image_button, (750, cheer_pos_y-25))

        font = pygame.font.Font(self.font_style, 65)
        if self.lang == 0:
            text_surface = font.render("ボタンを連打して", True, color)
            self.screen.blit(text_surface, (950, cheer_pos_y))
            text_surface = font.render("3Dプリンタを応援しよう！", True, color)
            self.screen.blit(text_surface, (950, cheer_pos_y+100))
        elif self.lang == 1:
            text_surface = font.render("Let's cheer for the 3D printer", True, color)
            self.screen.blit(text_surface, (950, cheer_pos_y))
            text_surface = font.render("by hitting the button!!", True, color)
            self.screen.blit(text_surface, (950, cheer_pos_y+100))


        # スピードプログレスバー

        # スピードプログレスバーの設定
        bar_speed_position = (1000, 700)
        bar_speed_size = (600, 50)

        c = self.printer.feedrate
        m = 300
        #font = pygame.font.Font(None, 64)

        font = pygame.font.Font(self.font_style, 50)
        if self.lang == 0:
            t = "造形速度 : " + str(c) + " / " + str(m) + " %"
        elif self.lang == 1:
            t = "Printing Speed : " + str(c) + " / " + str(m) + " %"
        text_surface = font.render(t , True, color)
        self.screen.blit(text_surface, (bar_speed_position[0], bar_speed_position[1] - 50))

        pygame.draw.rect(self.screen, WHITE, (bar_speed_position[0], bar_speed_position[1], bar_speed_size[0], bar_speed_size[1]))
        pygame.draw.rect(self.screen, RED, (bar_speed_position[0], bar_speed_position[1], bar_speed_size[0] * (c / m), bar_speed_size[1]))
        pygame.draw.rect(self.screen, BLACK, (bar_speed_position[0], bar_speed_position[1], bar_speed_size[0], bar_speed_size[1]), 2)

        # プログレスバー
        c , m = self.printer.get_progress()
        #font = pygame.font.Font(None, 64)
        font = pygame.font.Font(self.font_style, 64)
        t = "Progress : " + str(c) + " / " + str(m)
        text_surface = font.render(t , True, color)
        self.screen.blit(text_surface, (bar_position[0], bar_position[1] - 80))


        pygame.draw.rect(self.screen, WHITE, (bar_position[0], bar_position[1], bar_size[0], bar_size[1]))
        pygame.draw.rect(self.screen, GREEN, (bar_position[0], bar_position[1], bar_size[0] * (c / m), bar_size[1]))
        pygame.draw.rect(self.screen, BLACK, (bar_position[0], bar_position[1], bar_size[0], bar_size[1]), 2)


        # 造形対象の画像表示
        #print(self.images[self.selected_index])
        img = self.images[self.selected_index]
        self.screen.blit(img, (150, 200))


        # 温度の表示
        self.drawAll()
        self.drawGrid()

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
