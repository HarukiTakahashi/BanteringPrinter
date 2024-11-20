import pygame

class TetrisEdit():

    def __init__(self, s, gx, gy):
        self.screen = s

        self.grid_num_x = gx
        self.grid_num_y = gy

        self.offset_x = 0
        self.offset_y = 0

        self.grid_size = 30

        self.grid = [[0] * gy for _ in range(gx)]

    def draw(self):
    # 配列に基づいてグリッドを描画
        for row in range(self.grid_num_y):
            for col in range(self.grid_num_x):
                x = self.offset_x + col * self.grid_size 
                y = self.offset_y + row * self.grid_size 
                if self.grid[row][col] == 1:
                    pygame.draw.rect(self.screen, (0,255,0), (x, y, self.grid_size, self.grid_size))
                pygame.draw.rect(self.screen, (0,0,0), (x, y, self.grid_size, self.grid_size), 1)  # グリッド線

    def set_oofset(self,x,y):
        self.offset_x = x
        self.offset_y = y

    def toggle(self, x, y):
        self.grid[y][x] = 1 - self.grid[y][x]

    
    