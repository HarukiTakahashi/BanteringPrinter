import os, sys
import pygame
import random
import time
from printer import Printer

# シーンの基底クラス
class Scene():
    
    def __init__(self, s):
        self.screen = s
        self.name = "base"
        self.active = False
        pass
    
    def draw(self):
        pass
        
    