import pygame

class TetrisEdit():

    def __init__(self, s, grid_num_x=4, grid_num_y=4,grid_size = 50):
        self.screen = s

        self.grid_num_x = grid_num_x
        self.grid_num_y = grid_num_y

        self.grid_size = grid_size
        

        self.grid = [[0] * grid_num_y for _ in range(grid_num_x)]

    def draw(self, ox, oy):
        GRAY = (200,200,200)
        BLACK = (0,0,0)
        WHITE=(255,255,255)
        LIGHT_YELLOW = (255,255,100)
        RED = (255,0,0)
        
    # 配列に基づいてグリッドを描画
        for row in range(self.grid_num_y):
            for col in range(self.grid_num_x):
                x = ox + col * self.grid_size 
                y = oy + row * self.grid_size 
                if self.grid[row][col] == 1:
                    pygame.draw.rect(self.screen, RED, (x, y, self.grid_size, self.grid_size))
                else:
                    pygame.draw.rect(self.screen, GRAY, (x, y, self.grid_size, self.grid_size))
                pygame.draw.rect(self.screen, BLACK, (x, y, self.grid_size, self.grid_size), 1)  # グリッド線


    def toggle(self, pos):
        x = pos[0]
        y = pos[1]
        self.grid[y][x] = 1 - self.grid[y][x]

    
    