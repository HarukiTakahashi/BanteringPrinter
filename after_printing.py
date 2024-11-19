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
    MES_FLIP_TIME = 10 # sec

    # 温度設定
    safe_nozzle_temp = 50
    safe_bed_temp = 45
    
    sleep_amout = 3

    def __init__(self, s):
        super().__init__(s)
        self.name = "AfterPrinting"
        self.scene_num = 2
        self.holdtime = 0
        self.mes_flag = 0
        
        self.cur_time = int(time.time())
        
    def set_image_nozzle(self, img):
        self.image_nozzle = img
        
    def set_image_bed(self, img):
        self.image_bed = img

    def set_image_arrow(self, img):
        self.image_arrow= img

    def draw(self):
        
        
        if int(time.time()) - self.cur_time >= AfterPrinting.MES_FLIP_TIME: 
            self.mes_flag = 1 - self.mes_flag
            self.cur_time = int(time.time())

        # 色の定義
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLUE = (0, 50, 255)
        BLACK = (0, 0, 0)
        PINK = (255,100,100)
        



        # 画面設定
        width = self.screen.get_width()
        height = self.screen.get_height()

        font = pygame.font.Font(None, 36)
            
        self.screen.fill((255, 255, 255))
        color = (0, 0, 0)
        bg_color = (255, 255, 255)

        # 画像の位置設定
        img_margin = 100
        img_size = 450
        offset_y = -70
        img_position = (width//2 - img_size // 2, 
                        height // 2- img_size // 2 + offset_y)
        img_left_x = img_position[0] - img_size - img_margin
        img_right_x = img_position[0] + img_size + img_margin

        self.screen.blit(self.remove_images[0], 
                         (img_left_x, img_position[1]))
        self.screen.blit(self.remove_images[1], 
                         (img_position[0], img_position[1]))
        self.screen.blit(self.remove_images[2], 
                         (img_right_x, img_position[1])) 
        
        # font = pygame.font.Font(None, 64)

        font = pygame.font.Font(self.font_style, 64)
        if self.printer.bed_temp > AfterPrinting.safe_bed_temp:
            if self.lang == 0:
                text_surface = font.render("プリント完了！冷却中です…しばらくお待ちください", True, RED)
            elif self.lang == 1:
                text_surface = font.render("Completed! Cooling down, please wait a while!", True, RED)
            self.screen.blit(text_surface, (200, img_position[1]-100))
        else:
            if self.mes_flag == 0:
                if self.lang == 0:
                    text_surface = font.render("冷却完了！印刷物の取り外しにご協力ください！", True, BLUE)
                elif self.lang == 1:
                    text_surface = font.render("Completed! Help us remove the object!", True, BLUE)
            else:
                if self.lang == 0:
                    text_surface = font.render("印刷物を回収したらボタンを押してください！", True, BLUE)
                elif self.lang == 1:
                    text_surface = font.render("Press the button after collecting the object.", True, BLUE)
            self.screen.blit(text_surface, (200, img_position[1]-100))
       
        font = pygame.font.Font(self.font_style, 36)
        if self.lang == 0:
            if self.printer.nozzle_temp > AfterPrinting.safe_nozzle_temp:
                text_surface = font.render("" + str(self.printer.nozzle_temp) + " ℃", True, RED)
            else:
                text_surface = font.render("" + str(self.printer.nozzle_temp) + " ℃", True, BLUE)    
        elif self.lang == 1:
            if self.printer.nozzle_temp > AfterPrinting.safe_nozzle_temp:
                text_surface = font.render("" + str(self.printer.nozzle_temp) + " degC", True, RED)
            else:
                text_surface = font.render("" + str(self.printer.nozzle_temp) + " degC", True, BLUE)
 
        self.screen.blit(self.image_nozzle, (img_left_x+190, 390))            
        self.screen.blit(text_surface, (img_left_x+250, 400))

        if self.lang == 0:
            if self.printer.bed_temp > AfterPrinting.safe_bed_temp:
                text_surface = font.render("" + str(self.printer.bed_temp) + " ℃", True, RED)
            else:
                text_surface = font.render("" + str(self.printer.bed_temp) + " ℃", True, BLUE)    
        elif self.lang == 1:
            if self.printer.bed_temp > AfterPrinting.safe_bed_temp:
                text_surface = font.render("" + str(self.printer.bed_temp) + " degC", True, RED)
            else:
                text_surface = font.render("" + str(self.printer.bed_temp) + " degC", True, BLUE)    
        
        self.screen.blit(self.image_bed, (img_left_x+190, img_position[1] + img_size//2 + 110))            
        self.screen.blit(text_surface, (img_left_x+250, img_position[1] + img_size//2 + 120))

        font = pygame.font.Font(self.font_style, 24)
        if self.lang == 0:
            text_surface = font.render("温度が下がるまでお待ち下さい。", True, color)            
        elif self.lang == 1:
            text_surface = font.render("Wait until the nozzle and bed cool down.", True, color)
        self.screen.blit(text_surface, (img_left_x, img_position[1] + img_size+60))
        
        if self.lang == 0:
            text_surface = font.render("高温時は触れないでください！", True, RED)
        elif self.lang == 1:
            text_surface = font.render("Don't touch them at high temperatures!", True, RED)
        self.screen.blit(text_surface, (img_left_x, img_position[1] + img_size+100))


        # 真ん中のメッセージ
        if self.lang == 0:
            text_surface = font.render("プリントされた印刷物を取ってください。", True, color)
        elif self.lang == 1:
            text_surface = font.render("Remove the printed object from the bed.", True, color)
        self.screen.blit(text_surface, (img_position[0], img_position[1] + img_size+60))

        if self.lang == 0:
            text_surface = font.render("印刷物は差し上げます。", True, RED)
        elif self.lang == 1:
            text_surface = font.render("You can take it.", True, RED)
        self.screen.blit(text_surface, (img_position[0], img_position[1] + img_size+100))

        # 右のメッセージ
        if self.lang == 0:
            text_surface = font.render("ベッドが正しい位置に配置されており、", True, color)
        elif self.lang == 1:
            text_surface = font.render("Make sure the bed is in the correct position", True, color)
        self.screen.blit(text_surface, (img_right_x, img_position[1] + img_size+60))
        
        if self.lang == 0:
            text_surface = font.render("なにも残っていないことを確認してください。", True, color)
        elif self.lang == 1:
            text_surface = font.render("and there is nothing on it", True, color)
        self.screen.blit(text_surface, (img_right_x, img_position[1] + img_size+100))
        


        font = pygame.font.Font(self.font_style, 22)
        if self.printer.bed_temp < AfterPrinting.safe_bed_temp:
            # 矢印
            self.screen.blit(self.image_arrow, (1190,830))

            if self.lang == 0:
                text_surface = font.render("次の造形のためにボタンを押してください", True, RED)
            elif self.lang == 1:
                text_surface = font.render("Hold the button for the next print", True, RED)
            self.screen.blit(text_surface, (img_right_x, img_position[1] + img_size+200))

        # プログレスバー   
        bar_size = (400, 100)
        bar_position = (width//2 - bar_size[0] // 2, height//2+320)
    
        pygame.draw.rect(self.screen, WHITE, 
                         (bar_position[0], bar_position[1], bar_size[0], bar_size[1]))
        pygame.draw.rect(self.screen, PINK, 
                         (bar_position[0], bar_position[1], bar_size[0] * (self.holdtime / AfterPrinting.HOLD_TIME_MAX), bar_size[1]))
        pygame.draw.rect(self.screen, BLACK, 
                         (bar_position[0], bar_position[1], bar_size[0], bar_size[1]), 2)


        if self.is_cooled():

            font = pygame.font.Font(self.font_style, 42)
            if self.lang == 0:
                text_surface = font.render("作業完了！", True, color)
                self.screen.blit(text_surface, (width//2-90, bar_position[1]+10))
            elif self.lang == 1:
                text_surface = font.render("Completed!", True, color)
                self.screen.blit(text_surface, (width//2-130, bar_position[1]+10))


            font = pygame.font.Font(self.font_style, 28)
            if self.lang == 0:
                text_surface = font.render("ボタンを長押し (3秒間)", True, color)
            elif self.lang == 1:
                text_surface = font.render("Hold the button! (3 sec)", True, color)
            
            self.screen.blit(text_surface, (width//2-155, bar_position[1]+60))

        else:
            font = pygame.font.Font(self.font_style, 42)
            if self.lang == 0:
                text_surface = font.render("冷却中！", True, color)
            elif self.lang == 1:
                text_surface = font.render("Cooling!", True, color)
        
            self.screen.blit(text_surface, (width//2-90, bar_position[1]+10))


        # 作業完了
        if self.is_confirmed():
            BUBBLE_COLOR = (230, 230, 100)  # 吹き出しの色

             # 吹き出しのテキスト
            text = " Thank you! "
            font = pygame.font.Font(None, 120)
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect()

            bubble_padding = 20
            bubble_rect = pygame.Rect((bar_position[0]-70,bar_position[1] - 150), 
                                      (text_rect.width + bubble_padding*2, text_rect.height + 2 * bubble_padding))
        
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


    def set_image(self, img: list):
        self.remove_images = img

    def press(self):
        pass

    def stop(self):
        self.draw()

        time.sleep(AfterPrinting.sleep_amout)

    def hold_button(self):
        if self.is_cooled():
            self.holdtime+=1

    def release_button(self):
        self.holdtime = 0
    
    def is_confirmed(self):
        if self.holdtime >= AfterPrinting.HOLD_TIME_MAX:
            return True
        else:
            return False

    def is_cooled(self):
        if self.printer.bed_temp > AfterPrinting.safe_bed_temp:
            return False
        else:
            return True