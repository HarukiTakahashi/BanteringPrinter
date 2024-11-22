import os, sys
import pygame
import random
import time
from printer import Printer
from scene_base import Scene

# 造形中のクラス
class DuringPrinting(Scene):
    
    HOLD_TIME_MAX = 180
    HOLD_TIME_THREASHOLD = 60

    def __init__(self, s):
        super().__init__(s)
        self.name = "DuringPrinting"
        self.gcode_file_name = ""
        self.scene_num = 1
        self.image_button = None
        self.speed_up_amout = 10
        self.holdtime = 0
        self.timer = 0

    def set_image_button(self, img):
        self.image_button = img
    
    def set_image_nozzle(self, img):
        self.image_nozzle = img
        
    def set_image_bed(self, img):
        self.image_bed = img

    def set_image_check_man(self, img):
        self.image_check = pygame.transform.scale(img, (500, 500))

    def draw(self):

        # 色の定義
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        RED_A = (255, 230, 230)
        RED_A = (255, 230, 230,)
        BLACK = (0, 0, 0)
        ORANGE = (241,90,34)
        # 画面設定
        width = self.screen.get_width()
        height = self.screen.get_height()


        #font = pygame.font.Font(None, 80)
            
        self.screen.fill((255, 255, 255))
        rect = pygame.Rect(100, 100,width - 200, 400)
        color = (0, 0, 0)
        bg_color = (255, 255, 255)

        pygame.draw.rect(self.screen, bg_color, rect)

        font = pygame.font.Font(self.font_style, 80)
        if self.printer.is_starting_up:
            if self.lang == 0:
                text_surface = font.render("プリント準備中！", True, RED)
            elif self.lang == 1:
                text_surface = font.render("Now Preparing!", True, RED)
        elif self.printer.is_waiting:
            if self.lang == 0:
                text_surface = font.render("プリント準備中！", True, RED)
            elif self.lang == 1:
                text_surface = font.render("Now Preparing!", True, RED)
        else:
            if self.lang == 0:
                text_surface = font.render("プリント中!", True, color)
            elif self.lang == 1:
                text_surface = font.render("Now Printing!", True, color)
        self.screen.blit(text_surface, (750, 200))

        # ファイル名の表示
        font = pygame.font.Font(self.font_style, 60)
        #text_surface = font.render(" -> " + self.gcode_file_name, True, color)
        #self.screen.blit(text_surface, (800, 250))


        # 連打か温度上昇の表示!!!
        if self.printer.is_waiting or self.printer.is_starting_up:
            # 温度上昇中の温度計表示

            #self.image_nozzle = pygame.transform.scale(self.image_nozzle, (200, 200))
            self.screen.blit(self.image_nozzle, (800, 350))
            #self.image_bed = pygame.transform.scale(self.image_nozzle, (200, 200))
            self.screen.blit(self.image_bed, (800, 500))

            bar_noz_pos = (950,375)
            bar_bed_pos = (950,525)
            bar_size = (600,50)

            noz_max = 250
            noz_temp = self.printer.nozzle_temp
            bed_max = 120
            bed_temp = self.printer.bed_temp

            # TODO: とりあえず
            noz_target = 220
            bed_target = 60

            pygame.draw.rect(self.screen, WHITE, (bar_noz_pos[0], bar_noz_pos[1], bar_size[0], bar_size[1]))
            pygame.draw.rect(self.screen, RED, (bar_noz_pos[0], bar_noz_pos[1], bar_size[0] * (noz_temp / noz_max), bar_size[1]))
            pygame.draw.rect(self.screen, BLACK, (bar_noz_pos[0], bar_noz_pos[1], bar_size[0], bar_size[1]), 2)

            pygame.draw.rect(self.screen, WHITE, (bar_bed_pos[0], bar_bed_pos[1], bar_size[0], bar_size[1]))
            pygame.draw.rect(self.screen, RED, (bar_bed_pos[0], bar_bed_pos[1], bar_size[0] * (bed_temp / bed_max), bar_size[1]))
            pygame.draw.rect(self.screen, BLACK, (bar_bed_pos[0], bar_bed_pos[1], bar_size[0], bar_size[1]), 2)



            # 温度の矢印
            font = pygame.font.Font(self.font_style, 24)
            nx = bar_noz_pos[0] + bar_size[0] * (noz_target / noz_max)

            text_surface = font.render(str(noz_target)+"℃", True, color)
            text_rect = text_surface.get_rect()
            self.screen.blit(text_surface, (nx-text_rect.centerx,bar_noz_pos[1]-50))

            pygame.draw.polygon(self.screen, BLACK, [
                (nx-20,bar_noz_pos[1]-20),
                (nx,bar_noz_pos[1]),
                (nx+20,bar_noz_pos[1]-20)
                ], 0)
            
            nx = bar_bed_pos[0] + bar_size[0] * (bed_target / bed_max)

            text_surface = font.render(str(bed_target)+"℃", True, color)
            text_rect = text_surface.get_rect()
            self.screen.blit(text_surface, (nx-text_rect.centerx,bar_bed_pos[1]-50))

            pygame.draw.polygon(self.screen, BLACK, [
                (nx-20,bar_bed_pos[1]-20),
                (nx,bar_bed_pos[1]),
                (nx+20,bar_bed_pos[1]-20)
                ], 0)



            # 温度をバーで表示
            # 基準となる温度に色を付けておく
        else:
            # 造形中のボタン連打表示

            # ボタン画像
            cheer_pos_y = 350
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

            # スピードプログレスバーの設定
            bar_speed_position = (900, 625)
            bar_speed_size = (600, 50)

            c = self.printer.feedrate
            m = 100
            #font = pygame.font.Font(None, 64)

            font = pygame.font.Font(self.font_style, 50)
            if self.lang == 0:
                t = "プリント速度 : "
            elif self.lang == 1:
                t = "Printing Speed : "
            text_surface = font.render(t , True, color)
            text_rect_1 = text_surface.get_rect()
            self.screen.blit(text_surface, (bar_speed_position[0], bar_speed_position[1] - text_rect_1.height))

            font = pygame.font.Font(self.font_style, 50)
            t = "" + str(c)
            if c >= 100 and c < 200:
                 font = pygame.font.Font(self.font_style, 70)
                 text_surface = font.render(t , True, color)
            elif c >= 200  and c < 300:
                 font = pygame.font.Font(self.font_style, 80)
                 text_surface = font.render(t , True, ORANGE)
            elif c >= 300 and c < 400:
                 font = pygame.font.Font(self.font_style, 90)
                 text_surface = font.render(t , True, ORANGE)
            elif c >= 400:
                 font = pygame.font.Font(self.font_style, 100)
                 text_surface = font.render(t , True, RED)
            else:
                 text_surface = font.render(t , True, color)               
            
            text_rect_2 = text_surface.get_rect()
            self.screen.blit(text_surface, (bar_speed_position[0] + text_rect_1.width, 
                                            bar_speed_position[1] - text_rect_2.height))

            font = pygame.font.Font(self.font_style, 50)
            t = " / " + str(m) + " %"
            text_surface = font.render(t , True, color)
            self.screen.blit(text_surface, (bar_speed_position[0] + text_rect_1.width + text_rect_2.width,
                                             bar_speed_position[1] - text_rect_1.height))

            pygame.draw.rect(self.screen, WHITE, (bar_speed_position[0], bar_speed_position[1], bar_speed_size[0], bar_speed_size[1]))
            pygame.draw.rect(self.screen, RED, (bar_speed_position[0], bar_speed_position[1], bar_speed_size[0] * (c / m), bar_speed_size[1]))
            pygame.draw.rect(self.screen, BLACK, (bar_speed_position[0], bar_speed_position[1], bar_speed_size[0], bar_speed_size[1]), 2)

        # プログレスバーの設定
        prg_x_pos = 100
        bar_position = (prg_x_pos, height-200)
        bar_size = (width-400, 50)        
 
        # プログレスバー
        c , m = self.printer.get_progress()
        #font = pygame.font.Font(None, 64)

        font = pygame.font.Font(self.font_style, 58)
        tc = m-c
        if tc < 0: 
            tc = 0

        if self.lang == 0:
            t = "プリント完了まで : " + str(tc) + " / " + str(m)
        elif self.lang == 1:
            t = "To completion of printing : " + str(tc) + " / " + str(m)
        text_surface = font.render(t , True, color)
        self.screen.blit(text_surface, (bar_position[0], bar_position[1] - 80))

        pygame.draw.rect(self.screen, WHITE, (bar_position[0], bar_position[1], bar_size[0], bar_size[1]))
        pygame.draw.rect(self.screen, GREEN, (bar_position[0], bar_position[1], bar_size[0] * (tc / m), bar_size[1]))
        pygame.draw.rect(self.screen, BLACK, (bar_position[0], bar_position[1], bar_size[0], bar_size[1]), 2)


        # 造形対象の画像表示

        rect_x = 150
        rect_y = 200

        #print(self.images[self.selected_index])
        img = self.images[self.selected_index]
        self.screen.blit(img, (rect_x, rect_y))

        # チェックおじさん描画
        rect_w = 500
        rect_h = 500
        alpha = 200

        # チェックの発動条件
        # 10%ぐらい造形が進んでいることを条件にする？
        if self.holdtime > DuringPrinting.HOLD_TIME_THREASHOLD:
            ht = self.holdtime-DuringPrinting.HOLD_TIME_THREASHOLD
            if not self.printer.is_starting_up:

                rect_surface = pygame.Surface((rect_w,rect_h), pygame.SRCALPHA) 
                rect_surface.set_alpha(alpha)  # アルファ（透明度）を設定
                rect_surface.fill(WHITE)  # 四角形の色を設定

                border_thickness = 20  # 枠線の太さ
                self.screen.blit(rect_surface, (rect_x,rect_y))
                pygame.draw.rect(self.screen, RED_A, (rect_x,rect_y,
                                                    rect_w * (ht/DuringPrinting.HOLD_TIME_MAX),rect_h))
                pygame.draw.rect(self.screen, ORANGE, (rect_x,rect_y,rect_w,rect_h), border_thickness)

                font = pygame.font.Font(self.font_style, 82)
                self.screen.blit(self.image_check, (rect_x, rect_y))

                if ht > DuringPrinting.HOLD_TIME_MAX:
                    print("STOP AND OBSERVE!!!")
        

        # 温度の表示
        self.drawAll()
        self.drawGrid()
        pygame.display.update()

    def is_printing(self):
        return self.printer.is_printing()

    def press(self):
        a = self.printer.feedrate + self.speed_up_amout
        if a > 500:
            a = 500
        self.printer.change_feedrate(a)
       
    def set_gcode_file_name(self, f):
        self.gcode_file_name = f


    def set_timer(self):
        self.timer = time.time()
        
    def get_elasped_time(self):
        return time.time() - self.timer

    def hold_button(self):
        self.holdtime+=1

    def release_button(self):
        self.holdtime = 0