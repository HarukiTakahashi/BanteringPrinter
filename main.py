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
    printer.connect()
    printer.start_reading()
    printer.start_checking_temp()
    printer.start_checking_temp()
    printer.start_controlling_speed()
    
    # Scene 作成
    s_before = BeforePrinting(screen)
    s_before.set_printer(printer)
    s_before.set_items(items)
    s_before.active = True
    
    s_during = DuringPrinting(screen)
    s_during.set_printer(printer)
    
    s_after = AfterPrinting(screen)
    s_after.set_printer(printer)

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
                fname = s_before.get_file()
                s_during.set_gcode_file_name(fname)
                printer.open_gcode_file("gcode/" + fname)
                printer.start_printing()
                scene_stat = 1
                
        elif scene_stat == 1:
            # 造形中の状態
            s_during.draw()

            # 造形完了
            if not printer.is_printing:
                print("done")
                scene_stat = 2

            if pressed: 
                s_during.press()
                
        
        elif scene_stat == 2:
            # 造形後の状態
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