import os, sys
from pathlib import Path
import pygame
import random
import time
from printer import Printer
from before_printing import BeforePrinting
from during_printing import DuringPrinting
from after_printing import AfterPrinting


printer = None # Printerクラスのインスタンス
scenes = []

gcode_folder_path = ""

def main():
    global printer, gcode_folder_path

    scene_stat = 0 # シーンの状態管理

    # 初期化
    pygame.init()

    # 画面設定
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    
    pygame.display.set_caption('Title')

    # フォント設定
    font = pygame.font.Font(None, 36)

    # フォルダ内のファイルパスを取得
    gcode_folder_path = "./gcode"  # フォルダのパスを設定
    items = [f for f in os.listdir(gcode_folder_path) if os.path.isfile(os.path.join(gcode_folder_path, f))]

    # Printerクラスのインスタンス化
    printer = Printer()
    #printer.connect()
    #printer.start_reading()

    
    # Scene 作成
    s_before = BeforePrinting(screen)
    s_before.set_items(items)
    s_before.active = True
    
    s_during = DuringPrinting(screen)
    s_during.set_printer(printer)
    
    s_after = AfterPrinting(screen)


    # プログラムのメイン関数
    while True:
        pressed = False

        # マウス、キーボードなどの入力処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN): # and not selected:
                pressed = True

        if scene_stat == 0:
            # 造形前の状態
            s_before.draw()
            
            if pressed:
                s_before.stop()
                #printer.open_gcode_file("gcode/" + s_before.get_file())
                #printer.start_printing()
                scene_stat = 1
                
        elif scene_stat == 1:
            # 造形中の状態
            s_during.draw()
            
            if pressed: 
                s_during.press()
                scene_stat = 2
        
        elif scene_stat == 2:
            s_after.draw()
            
            if pressed: 
                s_after.press()
                s_before.active = True
                scene_stat = 0
        
        pygame.time.Clock().tick(60)
        


if __name__ == "__main__":
    try:
        main()

    finally:
        pygame.quit()
        printer.close_serial()
        print("hi")
        os._exit(-1) 