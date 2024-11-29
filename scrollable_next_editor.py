import os, sys
import pygame

import json
import random
import time
from scrollable import Scrollable
from tetris_edit import TetrisEdit

# class for making a scollable object
# this class is supposed to be inherited
class NextEditor(Scrollable):
    
    KEY_TO_POSITION = {
        pygame.K_1: (0,0), pygame.K_2: (1,0), pygame.K_3: (2,0), pygame.K_4: (3,0), pygame.K_5: (4,0), pygame.K_6: (5,0),
        pygame.K_q: (0,1), pygame.K_w: (1,1), pygame.K_e: (2,1), pygame.K_r: (3,1), pygame.K_t: (4,1), pygame.K_y: (5,1),
        pygame.K_a: (0,2), pygame.K_s: (1,2), pygame.K_d: (2,2), pygame.K_f: (3,2), pygame.K_g: (4,2), pygame.K_h: (5,2),
        pygame.K_z: (0,3), pygame.K_x: (1,3), pygame.K_c: (2,3), pygame.K_v: (3,3), pygame.K_b: (4,3), pygame.K_n: (5,3),                        
    }
    
    def __init__(self, screen, pos_start:tuple,pos_end:tuple, size=(100,100),candidate = 3):
        super().__init__(screen, pos_start,pos_end,size)
        
        self.candidate = candidate
        self.next_list = []
        self.current_next = 0      
        
        for i in range(candidate):
            t = TetrisEdit(self.screen,i)
            self.next_list.append(t)

    def control(self, keys):
        if keys.get(pygame.K_DOWN):
            if (not self.forwarding) and (not self.is_at_end):
                self.go_forward()
            else:
                self.go_backward()
                
        if self.is_at_end:
            if keys.get(pygame.K_LEFT):
                print("left")
                self.move_cursor(-1)
            if keys.get(pygame.K_RIGHT):
                print("right")
                self.move_cursor(1)   
                
            next_tetris = self.next_list[self.current_next]
            for key, (row, col) in NextEditor.KEY_TO_POSITION.items():
                if keys.get(key):  # キーが押されていれば
                    if row < next_tetris.grid_num_x and col < next_tetris.grid_num_y:
                        next_tetris.toggle((row,col))
                        
                        print("検証するよ！！")
                        #print(next_tetris.validate())
                        if next_tetris.validate():
                            next_tetris.making()

    def draw(self):
        BLACK = (0,0,0)
        WHITE=(255,255,255)
        LIGHT_YELLOW = (255,255,200)
        RED = (255,0,0)
        BLUE = (0,0,255)
        
        text = "NEXT"
        font = pygame.font.Font(self.font_style, 58)
        line_spacing = 60
        pygame.draw.rect(self.screen, LIGHT_YELLOW, [self.pos_x , self.pos_y, self.size[0],self.size[1]], 0)  # 線の太さ0は塗りつぶし
        pygame.draw.rect(self.screen, BLACK, [self.pos_x , self.pos_y, self.size[0],self.size[1]], 5)  # 線の太さ0は塗りつぶし

        pygame.draw.rect(self.screen, LIGHT_YELLOW, [self.pos_x-70,self.pos_y,70,len(text) * line_spacing], 0)  # inflateで少し余白を追加

        for i, char in enumerate(text):
            text_surface = font.render(char, True, BLACK)  # 文字を描画
            text_rect = text_surface.get_rect(topleft=(self.pos_x-60, self.pos_y + i * line_spacing))  # 各文字の位置
            self.screen.blit(text_surface, text_rect)  # 描画

        for i in range(self.candidate):
            te = self.next_list[i]
            x = self.pos_x+50
            y = self.pos_y+50 + (te.grid_size * te.grid_num_y + 50) * i
            te.draw(x,y)
            if self.current_next == i:
                pygame.draw.rect(self.screen, RED, [x,y,te.grid_size*te.grid_num_x,te.grid_size*te.grid_num_y], 5)

        text = "! Experimental !"
        font = pygame.font.Font(self.font_style, 36)
        text_surface = font.render(text, True, BLACK)  # 文字を描画
        text_rect = text_surface.get_rect(topleft=(self.pos_x+10, self.pos_y+self.size[1]-60))  # 各文字の位置
        self.screen.blit(text_surface, text_rect)

    def move_cursor(self, dir: int):
        self.current_next = (self.current_next + dir) % self.candidate
        if self.current_next < 0:
            self.current_next = self.candidate-1
        
        
    def remove(self):
        self.next_list.pop(0)
        t = TetrisEdit(self.screen,0)
        self.next_list.append(t)

        for i in range(self.candidate):
            self.next_list.num = i
        
