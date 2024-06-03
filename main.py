import os, sys
from pathlib import Path
import pygame
from pygame.locals import *
import random
import time
from printer import Printer
from before_printing import BeforePrinting
from during_printing import DuringPrinting
from after_printing import AfterPrinting
from nfc_read import NFCReading


printer = None # Printerクラスのインスタンス
nfc_read = None
scenes = []
gcode_folder_path = "./gcode" # Gcodeフォルダのパスを設定

def loadGcodeFiles():
    global printer, gcode_folder_path

    gcodes = [f for f in os.listdir(gcode_folder_path) if f.endswith('.gcode')]
    png_files = []
    
    for gcode_file in gcodes:
        base_name = os.path.splitext(gcode_file)[0]  # 拡張子を除いたファイル名
        corresponding_png = base_name + '.png'
        if corresponding_png in os.listdir(gcode_folder_path):
            png_files.append(corresponding_png)
        else:
            png_files.append('noimage.png')
    
    return gcodes, png_files



def main():
    global printer, nfc

    scene_stat = 0 # シーンの状態管理

    # 初期化
    pygame.init()

    # 画面設定
    width, height = 1920, 800 #1080
    screen = pygame.display.set_mode((width, height))
    #screen = pygame.display.set_mode((width, height),FULLSCREEN)
    
    pygame.display.set_caption('Title')

    # フォント設定
    font = pygame.font.Font(None, 36)

    # フォルダ内のファイルパスを取得
    gcode_file_list, png_file_list = loadGcodeFiles()
    print(gcode_file_list)
    print(png_file_list)

    img_list = []

    # 画像の読み込み
    for img_file in png_file_list:
        try:
            img = pygame.image.load(gcode_folder_path + "/" +img_file)
            img_list.append(img)
        except pygame.error as e:
            print(f"Error loading image {img_file}: {e}")

    # Printerクラスのインスタンス化
    printer = Printer()
    if printer.connect() == None:
        #print("cannot connect with a 3D printer")
        pass

    printer.start_reading()
    printer.start_checking_temp()
    printer.start_controlling_speed()

    # NFC_readクラスのインスタンス化
    nfc_read = NFCReading()
    nfc_read.start_reading()
    
    icon = pygame.image.load("image/icons.png")
    # Scene 作成
    # 造形開始前のシーン
    s_before = BeforePrinting(screen)
    s_before.set_printer(printer)
    s_before.set_nfc(nfc_read)
    s_before.set_gcode_file(gcode_file_list,img_list)
    s_before.load_icons(icon)
    s_before.roulette_active = True
    
    s_during = DuringPrinting(screen)
    s_during.set_printer(printer)
    s_during.set_nfc(nfc_read)
    s_during.set_gcode_file(gcode_file_list,img_list)
    s_during.set_image_button(pygame.image.load("image/button.png"))
    s_during.load_icons(icon)
    
    s_after = AfterPrinting(screen)
    s_after.set_printer(printer)
    s_after.set_nfc(nfc_read)
    s_after.set_gcode_file(gcode_file_list,img_list)
    s_after.load_icons(icon)

    aft_img = [pygame.image.load("image/after_1.png"),
               pygame.image.load("image/after_2.png"),
               pygame.image.load("image/after_3.png")
    ]
    s_after.set_image(aft_img)

    # プログラムのメイン関数
    while True:
        pressed = False
        clicked = False

        # マウス、キーボードなどの入力処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN): # and not selected:
                clicked = True
            
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            pressed = True

        if scene_stat == 0:
            # 造形前の状態

            s_before.draw()
            
            if clicked:
                # クリックされた
                s_before.stop()

                # シーン切り替えと造形開始前の処理
                fname, ind = s_before.get_file()
                s_during.set_gcode_file_name(fname)
                printer.open_gcode_file("gcode/" + fname)
                printer.start_printing()
 
                s_before.setIndexOfFile(ind)
                s_during.setIndexOfFile(ind)
                s_after.setIndexOfFile(ind)
                scene_stat = 1
                
        elif scene_stat == 1:
            # 造形中の状態
            s_during.draw()

            # 造形完了
            if not printer.is_printing:
                print("done")
                scene_stat = 2

            if clicked: 
                s_during.press()
                
        
        elif scene_stat == 2:
            # 造形後の状態
            s_after.draw()

            if s_after.is_confirmed():

                s_before.roulette_active = True
                s_after.holdtime = 0
                scene_stat = 0
            
            if pressed: 
                s_after.hold_button()
            else:
                s_after.release_button()

        
        pygame.time.Clock().tick(60)
        


if __name__ == "__main__":
    try:
        main()

    finally:
        pygame.quit()
        printer.close_serial()
        print("hi")
        os._exit(-1) 