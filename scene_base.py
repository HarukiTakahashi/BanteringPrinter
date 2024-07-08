import os, sys
import pygame
import random
import time

from printer import Printer
from nfc_read import NFCReading

# シーンの基底クラス
class Scene():
    
    DEBUG = False
    
    def __init__(self, s):
        self.screen = s
        self.name = "base"
        self.scene_num = -1
        self.active = False
        self.printer = None
        self.holdtime=-1

        self.selected_index = -1
        self.gcode_file = []
        self.images = []
        self.icons = []
        
        self.qr = None
        self.warn = None

        self.nfc_res = None
    
    def draw(self):
        pass
        
    # プリンタのインスタンスを設定
    def set_printer(self, p: Printer):
        self.printer = p
        
    # 言語設定
    def set_lang(self, i: int):
        self.lang = i

    def set_font(self, s: str):
        self.font_style = s
        
        
    # NFCのインスタンスを設定
    def set_nfc(self, n: NFCReading):
        self.nfc_res = n


    # 造形候補のGcodeファイル名と画像ファイル名を設定
    def set_gcode_file(self, g: list, img: list):
        self.gcode_file = list(g)
        self.images = list(img)

    def drawAll(self):
        self.drawTemperature()
        self.drawUserInfo()
        self.drawQR()
        self.drawProcess()
        self.drawWanring()
        pygame.display.flip()

    # プリンタの温度について表示
    def drawTemperature(self):
        
        #font = pygame.font.Font(None, 36)
        font = pygame.font.Font(self.font_style, 36)
        
        width = self.screen.get_width()
        height = self.screen.get_height()
        
        rect = pygame.Rect(100, height-200,200, height-100)

        if Scene.DEBUG:
            if self.lang == 0:
                text = "ノズル温度 : " + str(self.printer.nozzle_temp) + " ℃"
            elif self.lang == 1:
                text = "Nozzle temp : " + str(self.printer.nozzle_temp) + " degC"
                
            text_surface = font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (100,height-100))

            if self.lang == 0:
                text = "ベッド温度 : " + str(self.printer.bed_temp) + " ℃"
            elif self.lang == 1:
                text = "Bed temp : " + str(self.printer.bed_temp) + " degC"

            text_surface = font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (100,height-50))

            if self.lang == 0:
                text = "造形速度 : " + str(self.printer.feedrate) + "%"
            elif self.lang == 1:
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
        text_x_pos = 100
        text_w = 100
        text_h = 100
        text_h_margin = 25
        
        #font_u = pygame.font.Font(None, text_h)
        font_u = pygame.font.Font(self.font_style, 56)   
           
        if self.nfc_res.id_info != "":
            # ここのスライス表現が正しいかどうかチェック
            
            num = int(te)
            num = num // 10
            
            
            pygame.draw.rect(self.screen, (200,200,255), (0, 0, width, text_h))
            text_surface = font_u.render("    " + str(te), True, (0, 0, 0))
            self.screen.blit(text_surface, (text_x_pos,text_h_margin))
            if self.icons != None:
                self.screen.blit(self.icons[num%20], (40, -5))

        else:
            if self.lang == 0:
                te = "匿名ユーザ（学生証を置くと操作記録が残せます）"
            elif self.lang == 1:
                te = "Anonymous user (place your ID to log your operation)"
            
            pygame.draw.rect(self.screen, (200,200,200), (0, 0, width, text_h))
            text_surface = font_u.render("" + str(te), True, (0, 0, 0))
            self.screen.blit(text_surface, (text_x_pos,text_h_margin))


    # 造形プロセスを表示する
    def drawProcess(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        font_u = pygame.font.Font(self.font_style, 36)

        start_y = 25
        start_x = 1450
        box_w = 100
        box_h = 50
        margin = 15
        offset_x = 15

        LIGHT_ORANGE = (255,180,0)
        LIGHT_YELLOW = (255,255,224)
        GRAY = (150, 150, 150)
        BLACK = (0, 0, 0)
        te = ""

        for i in range(4):
            pygame.draw.rect(self.screen, LIGHT_YELLOW, (start_x+(margin+box_w)*i, start_y, box_w, box_h))

            if self.scene_num == i:
                pygame.draw.rect(self.screen, LIGHT_ORANGE, (start_x+(margin+box_w)*i, start_y, box_w, box_h))

            if i == 0:
                if self.lang == 0:
                    te = "開始"
                elif self.lang == 1:
                    te = "Start"
            if i == 1:
                if self.lang == 0:
                    te = "印刷"
                elif self.lang == 1:
                    te = "Print"
            if i == 2:
                if self.lang == 0:
                    te = "取外"
                elif self.lang == 1:
                    te = "Remove"
            if i == 3:
                if self.lang == 0:
                    te = "評価"
                elif self.lang == 1:
                    te = "Eval"

            if i == self.scene_num:
                text_surface = font_u.render("" + str(te), True, BLACK)
                self.screen.blit(text_surface, (start_x+(margin+box_w)*i + offset_x,start_y+5))
            else:
                text_surface = font_u.render("" + str(te), True, GRAY)
                self.screen.blit(text_surface, (start_x+(margin+box_w)*i + offset_x,start_y+5))



    # 画面にグリッドを表示
    # デバッグ用
    def drawGrid(self, g = 50):
        if not Scene.DEBUG:
            return
        
        GRAY = (200,200,200)
        grid_size = g
        width = self.screen.get_width()
        height = self.screen.get_height()
    
        # 縦のグリッド線を描画
        for x in range(0, width, grid_size):
            if x % 200 == 0:
                pygame.draw.line(self.screen, GRAY, (x, 0), (x, height),5)
            else:
                pygame.draw.line(self.screen, GRAY, (x, 0), (x, height))

        # 横のグリッド線を描画
        for y in range(0, height, grid_size):
            if y % 200 == 0:
                pygame.draw.line(self.screen, GRAY, (0, y), (width, y),5)
            else:
                pygame.draw.line(self.screen, GRAY, (0, y), (width, y))
                
        
    def drawQR(self):
        font = pygame.font.Font(self.font_style, 32)
        width = self.screen.get_width()
        height = self.screen.get_height()

        if self.lang == 0:
            text_surface = font.render("ご意見・ご要望・アンケートはこちらのQRから",True, (0, 0, 0))
        elif self.lang == 1:
            text_surface = font.render("     Send us your comments.",True, (0, 0, 0))
            
        self.screen.blit(text_surface, (width-900,height-100))

        if self.lang == 0:
            text_surface = font.render("プレイフルインタラクション研究室（高橋）",True, (0, 0, 0))
        elif self.lang == 1:
            text_surface = font.render("     Takahashi at Playful Lab. ",True, (0, 0, 0))
            
        self.screen.blit(text_surface, (width-900,height-50))
        self.screen.blit(self.qr,(width-210,height-210))
        
    def drawWanring(self):
        font = pygame.font.Font(self.font_style, 32)
        width = self.screen.get_width()
        height = self.screen.get_height()

        if self.lang == 0:
            text_surface = font.render("プリント中の3Dプリンタに手を触れないでください！",True, (0, 0, 0))
        elif self.lang == 1:
            text_surface = font.render("Don't touch a 3D printer while printing!",True, (0, 0, 0))
             
        self.screen.blit(text_surface, (140,height-75))
        self.screen.blit(self.warn,(20,height-110))

    def setIndexOfFile(self, i):
        self.selected_index = i
        
    def set_QR_image(self, img):
        self.qr = img

    def set_warning_image(self, img):
        self.warn = img
