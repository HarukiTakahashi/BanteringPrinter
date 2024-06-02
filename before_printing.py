import os, sys
import pygame
import random
import time
from printer import Printer
from scene_base import Scene
from nfc_read import NFCReading

# 造形前のクラス
class BeforePrinting(Scene):
    # アイテムを縦に並べるための数値
    item_size = 250
    item_num_line = 4
    margin = 60
    
    roulette_speed = 10
    sleep_amout = 1

    def __init__(self, s):
        super().__init__(s)
        self.name = "BeforePrinting"
        self.roulette_active = False
         
        self.highlight_index = 0
        self.roulette_coutner = 0
    
        # self.gcode_file = []
        # self.images = []


    def draw(self):

        # 描画する個数
        items_num = len(self.gcode_file)


        # ルーレット回転中
        if self.roulette_active:
            self.roulette_coutner += 1
            if self.roulette_coutner % BeforePrinting.roulette_speed == 0:
                self.highlight_index = (self.highlight_index + 1) % items_num


        # 画面サイズ
        width = self.screen.get_width()
        height = self.screen.get_height()

        images_per_row = BeforePrinting.item_num_line
        image_size = BeforePrinting.item_size
        margin = BeforePrinting.margin

        # グリッドのサイズを計算
        num_rows = (items_num + images_per_row - 1) // images_per_row
        grid_width = min(images_per_row, items_num) * (image_size + margin) - margin
        grid_height = num_rows * (image_size + margin) - margin

        # グリッドの左上の位置を計算（中央揃え）
        start_x = (width - grid_width) // 2
        start_y = (height - grid_height) // 2

        # 画像の読み込みとリサイズ
        img_list = [pygame.transform.scale(img, (image_size, image_size)) for img in self.images]


        # 画面塗りつぶし
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        font_64 = pygame.font.Font(None, 64)

        # 画像をグリッド状に描画
        for index, image in enumerate(img_list):
            row = index // images_per_row
            col = index % images_per_row
            x = start_x + col * (image_size + margin)
            y = start_y + row * (image_size + margin)
            self.screen.blit(image, (x, y))


            # 塗りつぶしのない矩形を描画
            if self.highlight_index == index:
                rect_color = (255, 0, 0)  # 黒色
                rect_position = (x, y, image_size, image_size)  # 矩形の位置とサイズ (x, y, width, height)
                border_thickness = 10  # 枠線の太さ
                pygame.draw.rect(self.screen, rect_color, rect_position, border_thickness)


            # ファイル名の描画
            file_name = os.path.splitext(self.gcode_file[index])[0]
            text_surface = font_64.render(file_name, True, (200, 0, 0))
            text_rect = text_surface.get_rect(center=(x + image_size // 2, y - 30))
            self.screen.blit(text_surface, text_rect)

        # ルーレットストップ時
        if not self.roulette_active:

            # 色の定義
            BLACK = (0, 0, 0)
            BUBBLE_COLOR = (230, 230, 100)  # 吹き出しの色

            # フォントの設定
            font_size = 120
            font_jp = pygame.font.SysFont("ipaexg.ttf", font_size)

            # 吹き出しのテキスト
            text = " Print this! "

            text_surface = font_jp.render(text, True, BLACK)
            text_rect = text_surface.get_rect()

            row = self.highlight_index // images_per_row
            col = self.highlight_index % images_per_row
            x = start_x + col * (image_size + margin) - image_size // 2
            y = start_y + row * (image_size + margin) - image_size / 2

            bubble_padding = 20
            bubble_rect = pygame.Rect((x,y), (text_rect.width + 2 * bubble_padding, text_rect.height + 2 * bubble_padding))


            thickness = 5

            # 吹き出しの本体部分
            pygame.draw.rect(self.screen, BUBBLE_COLOR, bubble_rect)
            #pygame.draw.rect(self.screen, BUBBLE_COLOR, bubble_rect,thickness)

            # 吹き出しの三角形の部分
            triangle_points = [
                (bubble_rect.centerx, bubble_rect.bottom+50),  # 三角形の先端
                (bubble_rect.centerx - 30, bubble_rect.bottom),  # 左の点
                (bubble_rect.centerx + 30, bubble_rect.bottom)  # 右の点
            ]
            pygame.draw.polygon(self.screen, BUBBLE_COLOR, triangle_points)
            #pygame.draw.polygon(self.screen, BUBBLE_COLOR, triangle_points,thickness)
            
            # テキストを吹き出しの中に描画
            text_position = (bubble_rect.left + bubble_padding, bubble_rect.top + bubble_padding)
            self.screen.blit(text_surface, text_position)


        # 画面の更新        
        self.drawTemperature()
        self.drawUserInfo()
        pygame.display.flip()
        
    # ルーレット停止処理
    def stop(self):
        self.roulette_active = False
        self.draw()

        time.sleep(BeforePrinting.sleep_amout)
        
    def get_file(self):
        return self.gcode_file[self.highlight_index], self.highlight_index
    
    

