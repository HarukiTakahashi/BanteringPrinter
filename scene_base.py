import os, sys
import pygame
import random
import time

from printer import Printer
from nfc_read import NFCReading

# シーンの基底クラス
class Scene():
    
    def __init__(self, s):
        self.screen = s
        self.name = "base"
        self.active = False
        self.printer = None

        self.selected_index = -1
        self.gcode_file = []
        self.images = []
        self.icons = []
        
        self.nfc_res = None
    
    def draw(self):
        pass
        
    # プリンタのインスタンスを設定
    def set_printer(self, p: Printer):
        self.printer = p
        
    # NFCのインスタンスを設定
    def set_nfc(self, n: NFCReading):
        self.nfc_res = n


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
        self.screen.blit(text_surface, (100,height-100))

        text = "Bed temperature : " + str(self.printer.bed_temp) + " deg C"
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (100,height-50))

        text = "Speed : " + str(self.printer.feedrate) + "%"
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (600,height-100))


    # アイコンの読み込み
    def load_icons(self, img):
        # 画像読み込み
        image = img

        # 分割する行と列の数
        rows, cols = 4, 6
        icon_width = 1600 // cols
        icon_height = 1200 // rows

        # リサイズ後のサイズ
        resized_width = 100
        resized_height = 100

        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col * icon_width, row * icon_height, icon_width, icon_height)
                icon = image.subsurface(rect)
                # 部分画像をリサイズ
                resized_icon = pygame.transform.scale(icon, (resized_width, resized_height))
                self.icons.append(resized_icon)


    # 学生証を読み込んだとき，学生の情報を出す
    def drawUserInfo(self):

        width = self.screen.get_width()
        height = self.screen.get_height()
        te = self.nfc_res.get_nfc_id()
        text_x_pos = 150
        text_w = 100
        text_h = 100
        text_h_margin = 25
        font_u = pygame.font.Font(None, text_h)     
           
        if self.nfc_res.id_info != "":
            # ここのスライス表現が正しいかどうかチェック
            num = int(te)
            pygame.draw.rect(self.screen, (200,200,255), (0, 0, width, text_h))
            text_surface = font_u.render("" + str(te), True, (0, 0, 0))
            self.screen.blit(text_surface, (text_x_pos,text_h_margin))
            if self.icons != None:
                self.screen.blit(self.icons[num%20], (40, 0))

        else:
            te = "Anonymous"
            
            pygame.draw.rect(self.screen, (200,200,200), (0, 0, width, text_h))
            text_surface = font_u.render("" + str(te), True, (0, 0, 0))
            self.screen.blit(text_surface, (text_x_pos,text_h_margin))



    def setIndexOfFile(self, i):
        self.selected_index = i