import os, sys
import pygame
import random
import time
from printer import Printer
from scene_base import Scene

# 造形前のクラス
class PrintingResult(Scene):
    HOLD_TIME_MAX = 30
    FINISH_TIME_MAX = 30

    roulette_speed = 60
    sleep_amout = 3
    
    EVALUATE_TIME_OUT = 20
    
    def __init__(self, s):
        super().__init__(s)
        self.name = "PrintingResult"
        self.scene_num = 3
        self.roulette_active = True
        self.highlight_index = 0
        self.roulette_coutner = 0
        self.holdtime = 0
        self.next_counter_time = 0
        
        self.stater = ""
        self.intervenor = []
        self.finisher = ""
        
        self.timeout_timer = 0
        
         
    def draw(self):
        # 色の定義
        WHITE = (255, 255, 255)
        GRAY = (200, 200, 200)
        GREEN = (0, 160, 0)
        RED = (255, 0, 0)
        RED_A = (255, 230, 230)
        BLUE = (200, 200, 255)
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

        #font = pygame.font.Font(None, 128)
        font = pygame.font.Font(self.font_style, 82)
        
        if self.lang == 0:
            text_surface = font.render("プリントした印刷物の出来はいかがですか?", True, color)
        elif self.lang == 1:
            text_surface = font.render("How does the printed object look?", True, color)
        self.screen.blit(text_surface, (150, 150))

        rect_w = 600
        rect_h = 300
        rect_margin = 200

        rect_left_x = width//2 - rect_w - rect_margin//2
        rect_right_x = width//2 + rect_margin//2
        rect_y = 280


        pygame.draw.rect(self.screen, BLUE, (rect_left_x,rect_y,rect_w,rect_h),10)
        pygame.draw.rect(self.screen, BLUE, (rect_right_x,rect_y,rect_w,rect_h),10)

        border_thickness = 20  # 枠線の太さ
        if self.highlight_index == 0:
            pygame.draw.rect(self.screen, RED_A, (rect_left_x,rect_y,
                                                  rect_w * (self.holdtime/PrintingResult.HOLD_TIME_MAX),rect_h))
            pygame.draw.rect(self.screen, RED, (rect_left_x,rect_y,rect_w,rect_h), border_thickness)
        elif self.highlight_index == 1:
            pygame.draw.rect(self.screen, RED_A, (rect_right_x,rect_y,
                                                  rect_w * (self.holdtime/PrintingResult.HOLD_TIME_MAX),rect_h))
            pygame.draw.rect(self.screen, RED, (rect_right_x,rect_y,rect_w,rect_h), border_thickness)


        font = pygame.font.Font(self.font_style, 82)
        text_surface = font.render("Good!", True, color)
        self.screen.blit(text_surface, (rect_left_x+50, rect_y+50))
        self.screen.blit(self.eval_images[0], (rect_left_x+rect_w-300, rect_y))

        text_surface = font.render("Bad!", True, color)
        self.screen.blit(text_surface, (rect_right_x+50, rect_y+50))
        self.screen.blit(self.eval_images[1], (rect_right_x+rect_w-300, rect_y))

        cont_y = 620

        if self.nfc_res.clf != None:
            font = pygame.font.Font(self.font_style, 42)
            text_surface = font.render("Contributors!", True, RED)
            self.screen.blit(text_surface, (200, cont_y))

            if self.lang == 0:
                text_surface = font.render("プリントを始めた人 : " + self.stater, True, BLACK)
            if self.lang == 1:
                text_surface = font.render("Started by : " + self.stater, True, BLACK)
            self.screen.blit(text_surface, (250, cont_y+50))        

            if self.lang == 0:
                text_surface = font.render("応援した人 : ", True, BLACK)
            if self.lang == 1:
                text_surface = font.render("Cheered by : ", True, BLACK)
            self.screen.blit(text_surface, (250, cont_y+100)) 
            
            text_intervenor = ""
            for i,s in enumerate(self.intervenor):
                text_intervenor = text_intervenor + "" + s
                if i < len(self.intervenor)-1:
                    text_intervenor += ", "

            text_surface = font.render(text_intervenor, True, BLACK)
            self.screen.blit(text_surface, (300, cont_y+150))        

            if self.lang == 0:
                text_surface = font.render("取り外した人 : " + self.finisher, True, BLACK)
            if self.lang == 1:
                text_surface = font.render("Finished by : " + self.finisher, True, BLACK)
            self.screen.blit(text_surface, (250, cont_y+200))        

            text_surface = font.render("... and You!", True, GREEN)
            self.screen.blit(text_surface, (300, cont_y+280))        

        # 印刷物がない場合はしばらくお待ちください
        c = PrintingResult.EVALUATE_TIME_OUT - (int(time.time()) - self.timeout_timer) 
        if c < 0:
            c = 0
        font = pygame.font.Font(self.font_style, 20)
        if self.lang == 0:
            text_surface = font.render("印刷物がない場合はしばらくお待ちください（" + str(c) + ")", True, BLACK)
        elif self.lang == 1:
            text_surface = font.render("Wait a moment if there is no printed object.（" + str(c) + ")", True, BLACK)
        self.screen.blit(text_surface, (width//2 + 350, rect_y-30))    
        
        # ルーレットストップ
        if self.is_confirmed():
            BUBBLE_COLOR = (230, 230, 100)  # 吹き出しの色

             # 吹き出しのテキスト
            text = " Thank you! "
            font = pygame.font.Font(None, 120)
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect()

            bubble_padding = 20

            if self.highlight_index == 0:
                bubble_rect = pygame.Rect((rect_left_x+150,rect_y - 150), (text_rect.width + 2 * bubble_padding, text_rect.height + 2 * bubble_padding))
            else:
                bubble_rect = pygame.Rect((rect_right_x+150,rect_y - 150), (text_rect.width + 2 * bubble_padding, text_rect.height + 2 * bubble_padding))
        
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



        self.drawAll()
        self.drawGrid()
        #pygame.display.flip()


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
        self.eval_images = img
        self.eval_images = [pygame.transform.scale(img, (image_size, image_size)) for img in self.eval_images]

    def set_starter(self, s: str):
        self.stater = s

    def set_intervenor(self, s: str):
        if not s in self.intervenor:
            self.intervenor.append(s)

    def reset_intervenor(self):
        self.intervenor = []

    def set_finisher(self, s: str):
        self.finisher = s

    def hold_button(self):
        self.holdtime+=1
        self.roulette_active = False

    def release_button(self):
        self.holdtime = 0
        self.roulette_active = True

    def is_confirmed(self):
        if self.holdtime >= PrintingResult.HOLD_TIME_MAX:
            return True
        else:
            return False
        
    def set_timeout(self):
        self.timeout_timer = int(time.time())
        
    def check_timeout(self):
        if int(time.time()) - self.timeout_timer > PrintingResult.EVALUATE_TIME_OUT:
            return True
        else:
            return False