import os, sys
import pygame
import random
import time

# class for making a scollable object
# this class is supposed to be inherited
class Scrollable():

    def __init__(self, screen, pos_start:tuple,pos_end:tuple, size=(100,100)):
        self.screen = screen
        self.start_pos = pos_start
        self.end_pos = pos_end
        self.size = size
        self.pos_x = pos_start[0]
        self.pos_y = pos_start[1]
        self.forwarding = False
        self.backwarding = False

        self.is_at_start = True
        self.is_at_end = False

    def draw(self):
        pygame.draw.rect(self.screen, (255,0,0), [self.pos_x , self.pos_y, self.size[0],self.size[1]], 0)  # 線の太さ0は塗りつぶし

        #pygame.display.flip()
    
    def move(self):
        
        if self.forwarding:
            self.forward()
            
        if self.backwarding:
            self.backward()
    
        self.is_at_end = False
        if abs(self.pos_x - self.end_pos[0]) < 1 and abs(self.pos_y - self.end_pos[1]) < 1:
            self.is_at_end = True
        
        self.is_at_start = False
        if abs(self.pos_x - self.start_pos[0]) < 1 and abs(self.pos_y - self.start_pos[1]) < 1:
            self.is_at_start = True
    
    def go_forward(self):
        self.forwarding = True
        self.backwarding = False
        
    def go_backward(self):
        self.backwarding = True
        self.forwarding = False
    
    def forward(self):
        base_easing = 0.2  # 初期速度
        min_easing = 0.1  # 最小速度 (止まらないように)
        dist_x = self.end_pos[0] - self.pos_x
        dist_y = self.end_pos[1] - self.pos_y
        dist = (dist_x**2 + dist_y**2)**0.5  # 距離の大きさ
        easing = max(base_easing * (1 - min(1, dist / 800)), min_easing)
    
        flag_x = False
        flag_y = False
        if abs(self.pos_x - self.end_pos[0]) < 1:
            self.pos_x = self.end_pos[0]
            flag_x = True
        else:
            self.pos_x += dist_x * easing
            
        if abs(self.pos_y - self.end_pos[1]) < 1:
            self.pos_y = self.end_pos[1]
            flag_y = True
        else:
            self.pos_y += dist_y * easing          
            
        if self.is_at_end:
            self.forwarding = False
        
    def backward(self):
        base_easing = 0.2  # 初期速度
        min_easing = 0.01  # 最小速度 (止まらないように)
        dist_x = self.start_pos[0] - self.pos_x
        dist_y = self.start_pos[1] - self.pos_y
        dist = (dist_x**2 + dist_y**2)**0.5  # 距離の大きさ
        easing = max(base_easing * (1 - min(1, dist / 800)), min_easing)
        
        flag_x = False
        flag_y = False
        if abs(self.pos_x - self.start_pos[0]) < 1:
            self.pos_x = self.start_pos[0]
            flag_x = True
        else:
            self.pos_x += dist_x * easing
            
        if abs(self.pos_y - self.start_pos[1]) < 1:
            self.pos_y = self.start_pos[1]
            flag_y = True
        else:
            self.pos_y += dist_y * easing         
    
        if self.is_at_start:
            self.backwarding = False
    
    def to_start(self):
        self.pos_x = self.start_pos[0]
        self.pos_y = self.start_pos[1]
    
    def to_end(self):
        self.pos_x = self.end_pos[0]
        self.pos_y = self.end_pos[1]

