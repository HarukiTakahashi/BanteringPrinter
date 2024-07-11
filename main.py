import os, sys
from pathlib import Path
import pygame
import logging
from pygame.locals import *
import random
import time, datetime
from printer import Printer
from before_printing import BeforePrinting
from during_printing import DuringPrinting
from after_printing import AfterPrinting
from printing_result import PrintingResult
from nfc_read import NFCReading


printer = None # Printerクラスのインスタンス
scenes = []
nfc_read = None
gcode_folder_path = "./gcode" # Gcodeフォルダのパスを設定
logger = None
FPS = 120

# 0: JP
# 1: EN
LANGUAGE = 0
FONT_STYLE = 'keifont.ttf'

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


# ログを残すようにしてみる
def setup_logger(log_file):
    # ロガーの設定
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)

    # ファイルハンドラの設定
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # フォーマットの設定
    formatter = logging.Formatter('%(asctime)s,%(message)s')
    file_handler.setFormatter(formatter)

    # ハンドラをロガーに追加
    logger.addHandler(file_handler)

    return logger

# ロガーにメッセージを送る関数
def log_message(logger, message=""):
    # 現在の時刻を取得してログに追加
    current_time = datetime.datetime.now().strftime('%Y/%m/%d, %H:%M:%S')
    log_entry = f'{current_time},{nfc_read.id_str},{message}'
    logger.info(log_entry)

def main():
    global printer, logger, nfc_read

    scene_stat = 0 # シーンの状態管理

    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,-100'

    # 初期化
    pygame.init()
    pygame.mixer.init()
    
    # 効果音ファイルの読み込み（例：effect.wav）
    sound_fx_pa = pygame.mixer.Sound('soundfx/pa.mp3')
    sound_fx_kin = pygame.mixer.Sound('soundfx/kin.mp3')
    sound_fx_kako = pygame.mixer.Sound('soundfx/kako.mp3')
    


    # 画面設定
    width, height = 1920, 1080 #1080
    screen = pygame.display.set_mode((width, height))
    #screen = pygame.display.set_mode((width, height),FULLSCREEN)
    
    pygame.display.set_caption('Title')

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

    nfc_read.set_fx_pikon(pygame.mixer.Sound('soundfx/pikon.mp3'))
    nfc_read.set_fx_bubu(pygame.mixer.Sound('soundfx/bubu.mp3'))
    
    icon = pygame.image.load("image/icons.png")
    qr = pygame.image.load("image/questionnaire.png")
    qr = pygame.transform.scale(qr, (200, 200))
    warn = pygame.image.load("image/warning.png")
    noz = pygame.image.load("image/nozzle.png")
    bed = pygame.image.load("image/bed.png")

    # Scene 作成
    scenes = []

    # 造形開始前のシーン
    s_before = BeforePrinting(screen)
    scenes.append(s_before)
    s_before.roulette_active = True
    s_before.set_image_button(pygame.image.load("image/button.png"))

    
    s_during = DuringPrinting(screen)
    scenes.append(s_during)
    s_during.set_image_button(pygame.image.load("image/button.png"))
    s_during.set_image_nozzle(noz)
    s_during.set_image_bed(bed)
       
    s_after = AfterPrinting(screen)
    s_after.set_image_nozzle(pygame.transform.scale(noz, (50, 50)))
    s_after.set_image_bed(pygame.transform.scale( bed, (50, 50)))
    scenes.append(s_after)

    s_result = PrintingResult(screen)
    scenes.append(s_result)

    for s in scenes:
        s.set_printer(printer)
        s.set_nfc(nfc_read)
        s.set_gcode_file(gcode_file_list,img_list)
        s.load_icons(icon)
        s.set_lang(LANGUAGE)
        s.set_font(FONT_STYLE)
        s.set_QR_image(qr)
        s.set_warning_image(warn)
        s.set_FPS(FPS)
    nfc_read.set_lang(LANGUAGE)

    aft_img = [pygame.image.load("image/after_1.png"),
               pygame.image.load("image/after_2.png"),
               pygame.image.load("image/after_3.png")
    ]
    s_after.set_image(aft_img)

    res_img = [pygame.image.load("image/result_good.png"),
               pygame.image.load("image/result_bad.png")
    ]
    s_result.set_image(res_img)


    # ロガーの設定
    log_file = 'log/system.log'
    logger = setup_logger(log_file)
    log_message(logger, message='System start')

    # プリントタスクごとのロガー
    task_file = ""
    task_logger = None

    pygame.time.Clock().tick(FPS)

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
                #log_message(logger, 'Gcode File Selected')

                # プリントタスクごとのロガー
                task_file = 'log/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".log"
                task_logger = setup_logger(task_file)

                # クリックされた
                sound_fx_pa.play()
                s_before.stop()

                # シーン切り替えと造形開始前の処理
                fname, ind = s_before.get_file()
                s_before.printer.change_feedrate(50)
                s_during.set_gcode_file_name(fname)
                printer.open_gcode_file("gcode/" + fname)
                printer.start_printing()
 
                s_before.setIndexOfFile(ind)
                s_during.setIndexOfFile(ind)
                s_after.setIndexOfFile(ind)
                scene_stat = 1

                # ログ
                log_message(task_logger, 'Print start,' + fname)
                s_result.set_starter(nfc_read.id_str)

        # 造形中の状態======================================================================
        elif scene_stat == 1:
            
        
            s_during.draw()
            #time.sleep(10)
            
            if not printer.serial.is_open:
                print("to scene 2")
                time.sleep(1)
                scene_stat = 2

            # 造形完了
            if not printer.is_printing:
                print("done")
                log_message(task_logger, 'Finish printing')
                scene_stat = 2

            if clicked: 
                s_during.press()
                sound_fx_kako.play()
                # ログ
                log_message(task_logger, 'Press button,' + str(printer.feedrate))
                s_result.set_intervenor(nfc_read.id_str)
        
        elif scene_stat == 2:
            # 造形後の状態
            s_after.draw()

            if s_after.is_confirmed():
                sound_fx_kin.play()
                s_after.stop()

                scene_stat = 3
                s_result.roulette_active = True
                
                s_after.holdtime = 0

                # ログ
                log_message(task_logger, 'Object removed')
                s_result.set_finisher(nfc_read.id_str)


            if pressed: 
                s_after.hold_button()
            else:
                s_after.release_button()

        elif scene_stat == 3:
            # 造形後の評価フェーズ
            s_result.draw()
            #print("hi")
            #time.sleep(1)

            if s_result.is_confirmed():
                # クリックされた
                sound_fx_pa.play()
                s_result.stop()

                s_result.holdtime = 0
                s_before.roulette_active = True
                s_result.reset_intervenor()
                scene_stat = 0

                # ログ
                log_message(task_logger, 'Evaluate object, ' + str(s_result.highlight_index))
                del(task_logger)

            if pressed: 
                s_result.hold_button()
            else:
                s_result.release_button()
        

if __name__ == "__main__":
    try:
        main()

    finally:
        pygame.quit()
        printer.close_serial()
        log_message(logger, message='System end')
        os._exit(-1) 
