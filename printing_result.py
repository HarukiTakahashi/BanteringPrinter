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
    roulette_speed = 60

    sleep_amout = 3
    
    def __init__(self, s):
        super().__init__(s)
        self.name = "PrintingResult"
        self.roulette_active = True
        self.highlight_index = 0
        self.roulette_coutner = 0
         
    def draw(self):
        # 色の定義
        WHITE = (255, 255, 255)
        GRAY = (200, 200, 200)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        BLACK = (0, 0, 0)
        PINK = (255,100,100)
        
        # 画面設定
        width = self.screen.get_width()
        height = self.screen.get_height()

        if self.roulette_active:
            self.roulette_coutner += 1
            if self.roulette_coutner % PrintingResult.roulette_speed == 0:
                self.highlight_index = (self.highlight_index + 1) % 2

        font = pygame.font.Font(None, 36)
            
        self.screen.fill((255, 255, 255))
        rect = pygame.Rect(100, 100,width - 200, 400)
        color = (0, 0, 0)
        bg_color = (255, 255, 255)

        bar_position = (width//2, height//2+300)

        font = pygame.font.Font(None, 128)
        text_surface = font.render("How does the printed object look?", True, color)
        self.screen.blit(text_surface, (width//2-500, height//2-300))

        rect_w = 600
        rect_h = 300
        rect_margin = 200

        rect_left_x = width//2 - rect_w - rect_margin//2
        rect_right_x = width//2 + rect_margin//2
        rect_y = height // 2

        pygame.draw.rect(self.screen, WHITE, (rect_left_x,rect_y,rect_w,rect_h),2)
        pygame.draw.rect(self.screen, WHITE, (rect_right_x,rect_y,rect_w,rect_h),2)

        border_thickness = 15  # 枠線の太さ
        if self.highlight_index == 0:
            pygame.draw.rect(self.screen, RED, (rect_left_x,rect_y,rect_w,rect_h), border_thickness)
        else:
            pygame.draw.rect(self.screen, RED, (rect_right_x,rect_y,rect_w,rect_h), border_thickness)


        font = pygame.font.Font(None, 128)
        text_surface = font.render("Good!", True, color)
        self.screen.blit(text_surface, (rect_left_x+50, rect_y+50))
        self.screen.blit(self.images[0], (rect_left_x+rect_w-300, rect_y))

        text_surface = font.render("Bad!", True, color)
        self.screen.blit(text_surface, (rect_right_x+50, rect_y+50))
        self.screen.blit(self.images[1], (rect_right_x+rect_w-300, rect_y))

        
        # ルーレットストップ
        if not self.roulette_active:
            BUBBLE_COLOR = (230, 230, 100)  # 吹き出しの色

             # 吹き出しのテキスト
            text = " Thank you! "
            font = pygame.font.Font(None, 120)
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect()

            bubble_padding = 20

            if self.highlight_index == 0:
                bubble_rect = pygame.Rect((rect_left_x+100,rect_y - 200), (text_rect.width + 2 * bubble_padding, text_rect.height + 2 * bubble_padding))
            else:
                bubble_rect = pygame.Rect((rect_right_x+100,rect_y - 200), (text_rect.width + 2 * bubble_padding, text_rect.height + 2 * bubble_padding))
        
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



        self.drawTemperature()
        self.drawUserInfo()
        pygame.display.flip()


    def press(self):
        pass

    # ルーレット停止処理
    def stop(self):
        self.roulette_active = False
        self.draw()
        self.roulette_coutner = 0

        time.sleep(PrintingResult.sleep_amout)

    def set_image(self, img: list):
        image_size = 300
        self.images = img
        self.images = [pygame.transform.scale(img, (image_size, image_size)) for img in self.images]
