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

from scrollable_next_editor import NextEditor


from nfc_read import NFCReading
from postSlack import Slack

printer = None # Printerクラスのインスタンス
scenes = []
nfc_read = None
key_input = {}
key_input_once = {}

gcode_folder_path = "./gcode_small_tetoris" # Gcodeフォルダのパスを設定
#gcode_folder_path = "./gcode" # Gcodeフォルダのパスを設定

logger = None
slack = None
FPS = 120

# 0: JP
# 1: EN
LANGUAGE = 0
FONT_STYLE = 'keifont.ttf'
NFC_ENABLE = False
SLACK_ENABLE = False

# Slack token
SLACK_TOKEN = ''
SLACK_CHANNEL = ''
SLACK_MEMBER_ID = '' 

# ボタン連打通知間隔(sec)
# ここに指定された時間以上経過しないとSlackへ通知されないように制限
BUTTON_TIME_SPAN = 60

# Gcodeファイルの読み込み
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

# ロガーの設定
def setup_logger(log_file):
    # ロガーの設定
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)

    # ファイルハンドラの設定
    file_handler = logging.FileHandler(log_file,encoding='utf-8')
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

# 初期化
def init():
    os.environ['SDL_VIDEO_WINDOW_POS'] = '1920,80'

# メイン関数 ========================================================================
def main():
    global printer, logger, nfc_read, slack, LANGUAGE

    scene_stat = 0 # シーンの状態管理

    
    # 初期化
    pygame.init()
    pygame.mixer.init()
    init()
    
    # 効果音ファイルの読み込み（例：effect.wav）
    sound_fx_pa = pygame.mixer.Sound('soundfx/pa.mp3')
    sound_fx_kin = pygame.mixer.Sound('soundfx/kin.mp3')
    sound_fx_kako = pygame.mixer.Sound('soundfx/kako.mp3')
    
    # 画面設定
    width, height = 1920, 1080 #1080
    #screen = pygame.display.set_mode((width, height))
    screen = pygame.display.set_mode((width, height),FULLSCREEN)
    
    pygame.display.set_caption('Title')

    # フォルダ内のファイルパスを取得
    gcode_file_list, png_file_list = loadGcodeFiles()
    print(gcode_file_list)
    print(png_file_list)


    # 画像の読み込み
    img_list = []
    for img_file in png_file_list:
        try:
            img = pygame.image.load(gcode_folder_path + "/" +img_file)
            img_list.append(img)
        except pygame.error as e:
            print(f"Error loading image {img_file}: {e}")

    # Printerクラスのインスタンス化
    printer = Printer()
    if printer.connect() == None:
        print("cannot connect with a 3D printer")
        pass

    printer.start_reading()
    printer.start_checking_temp()
    printer.start_controlling_speed()

    # NFC_readクラスのインスタンス化
    nfc_read = NFCReading()
    nfc_read.start_reading()
    nfc_read.set_fx_pikon(pygame.mixer.Sound('soundfx/pikon.mp3'))
    nfc_read.set_fx_bubu(pygame.mixer.Sound('soundfx/bubu.mp3'))
    nfc_read.set_lang(LANGUAGE)
    
    # Slackポスト用クラスのインスタンス化
    slack = Slack(SLACK_TOKEN, SLACK_CHANNEL,SLACK_MEMBER_ID)
    slack.enable(SLACK_ENABLE)
    
    # 画像の読み込み
    icon = pygame.image.load("image/icons.png")
    qr = pygame.image.load("image/questionnaire.png")
    qr = pygame.transform.scale(qr, (200, 200))
    warn = pygame.image.load("image/warning.png")
    noz = pygame.image.load("image/nozzle.png")
    bed = pygame.image.load("image/bed.png")
    arrow = pygame.image.load("image/arrow.png")

    # Scene 作成
    scenes = []

    # 造形開始前のシーン
    s_before = BeforePrinting(screen)
    scenes.append(s_before)
    s_before.roulette_active = True
    s_before.set_image_button(pygame.image.load("image/button.png"))

    # 造形中のシーン
    s_during = DuringPrinting(screen)
    scenes.append(s_during)
    s_during.set_image_button(pygame.image.load("image/button.png"))
    s_during.set_image_check_man(pygame.image.load("image/check_man.png"))
    s_during.set_image_nozzle(noz)
    s_during.set_image_bed(bed)
    
    # 造形後のシーン
    s_after = AfterPrinting(screen)
    scenes.append(s_after)
    s_after.set_image_nozzle(pygame.transform.scale(noz, (50, 50)))
    s_after.set_image_bed(pygame.transform.scale( bed, (50, 50)))
    s_after.set_image_arrow(pygame.transform.scale( arrow, (220, 100)))
    aft_img = [pygame.image.load("image/after_1.png"),
               pygame.image.load("image/after_2.png"),
               pygame.image.load("image/after_3.png")
    ]
    s_after.set_image(aft_img)


    # 評価のシーン
    s_result = PrintingResult(screen)
    scenes.append(s_result)
    res_img = [pygame.image.load("image/result_good.png"),
               pygame.image.load("image/result_bad.png")
    ]
    s_result.set_image(res_img)


    # シーンの設定
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
        
    # ロガーの設定
    log_file = 'log/system.log'
    logger = setup_logger(log_file)
    log_message(logger, message='System start')
    slack.post(":airplane_departure: システム起動\n")

    # プリントタスクごとのロガー
    task_file = ""
    task_logger = None

    pygame.time.Clock().tick(FPS)

    #printer.close_serial()

    # 長押しの判定時間（秒）
    hold_threshold = 0.5
    mouse_pressed_time = 0  # マウスが押された時刻
    pressed = False
    
    
    # 新機能実験 =============================
    sss = NextEditor(screen,(width,200),(width-300,200),(300,800))
    sss.set_font(FONT_STYLE)
    
    # ========================================
    
    
    # プログラムのメイン関数
    while True:

        clicked = False

        # マウス、キーボードなどの入力処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif (event.type == pygame.MOUSEBUTTONDOWN): # and not selected:
                # clicked = True
                mouse_pressed_time = time.time()  # 現在の時間を記録
                pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                # ボタンが押されてから離すまでの時間を計算
                hold_time = time.time() - mouse_pressed_time
                if hold_time >= hold_threshold:
                    print("Long hold detected")
                    pressed = False
                else:
                    clicked = True
                    pressed = False
                
                # 状態をリセット
                mouse_pressed_time = 0
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l: 
                LANGUAGE = 1 - LANGUAGE
                nfc_read.set_lang(LANGUAGE)
                for s in scenes:
                    s.set_lang(LANGUAGE)

            # KEYUP: キーを離したとき
            if event.type == pygame.KEYUP:
                key_input[event.key] = False
                key_input_once[event.key] = False  # フラグをリセット
            if event.type == pygame.KEYDOWN:
                # KEYDOWN: キーを押したとき
                key_input[event.key] = True
                # 押した瞬間の処理用フラグを立てる
                key_input_once[event.key] = True
                sss.control(key_input_once)
                        
        #mouse_buttons = pygame.mouse.get_pressed()
        #if mouse_buttons[0]:
        #    pressed = True

        if scene_stat == 0:
            # 造形前の状態

            s_before.draw()
            
            # 造形対象決定
            if clicked:
                #log_message(logger, 'Gcode File Selected')

                # プリントタスクごとのロガー
                d = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                task_file = 'log/' + d + ".log"
                task_logger = setup_logger(task_file)

                # シーン切り替えと造形開始前の処理
                fname, ind = s_before.get_file()

                # ログは可能な限り早く残す
                log_message(task_logger, 'Print start,' + fname)
                s_result.set_starter(nfc_read.id_str)


                # Slackにポスト
                slack.post(":bulb: 造形開始！\n"+fname)
                
                # クリックされた
                sound_fx_pa.play()

                # ここで処理が一時停止するのでログは事前にのこす
                s_before.stop()

                s_before.printer.change_feedrate(50)
                s_during.set_gcode_file_name(fname)
                printer.open_gcode_file(gcode_folder_path+"/" + fname)
                printer.start_printing()
 
                s_before.setIndexOfFile(ind)
                s_during.setIndexOfFile(ind)
                s_after.setIndexOfFile(ind)

                # 1だよ
                scene_stat = 1

        # 造形中の状態======================================================================
        elif scene_stat == 1:
        
            s_during.draw()

            if not printer.serial.is_open:
                print("to scene 2")
                time.sleep(1)
                scene_stat = 2

            # 造形完了
            if not printer.is_printing:
                print("done")
                log_message(task_logger, 'Finish printing')
                # Slackにポスト
                slack.post(":white_check_mark: 造形完了！\n")

                scene_stat = 2

            if clicked: 
                sound_fx_kako.play()

                if s_during.get_elasped_time() > 60:
                    # Slackにポスト
                    slack.post(":rotating_light: 造形中にボタンが押されました！\n",notification=False)
                s_during.set_timer()

                # ログ
                log_message(task_logger, 'Press button,' + str(printer.feedrate))
                s_result.set_intervenor(nfc_read.id_str)

                s_during.press()

            if pressed: 
                s_during.hold_button()
            else:
                s_during.release_button()
        
        elif scene_stat == 2:
            # 造形後の状態
            s_after.draw()

            # 評価フェーズへ
            if s_after.is_confirmed():
                sound_fx_kin.play()

                # ログ
                log_message(task_logger, 'Object removed')
                # Slackにポスト
                slack.post(":broom: 取り外し作業完了\n")
                
                s_result.set_finisher(nfc_read.id_str)

                s_after.stop()
                scene_stat = 3
                
                s_result.roulette_active = True
                s_result.highlight_index = 0
                s_result.roulette_coutner = 0                
                s_after.holdtime = 0
                
                s_result.set_timeout()

            if pressed: 
                s_after.hold_button()
            else:
                s_after.release_button()

        elif scene_stat == 3:
            # 造形後の評価フェーズ
            s_result.draw()
            #print("hi")
            #time.sleep(1)

            if s_result.is_confirmed() or s_result.check_timeout():
                # クリックされた
                sound_fx_pa.play() 

                if s_result.check_timeout():
                    s_result.highlight_index = -1

                # ログ
                log_message(task_logger, 'Evaluate object, ' + str(s_result.highlight_index))
                del(task_logger)
                # Slackにポスト
                slack.post(":100: 評価完了: " + str(s_result.highlight_index)+"\n===")
                
                s_result.stop()

                s_result.holdtime = 0
                s_before.roulette_active = True
                s_before.shuffle() # ルーレットの開始地点をシャッフルする
                s_result.reset_intervenor()
                scene_stat = 0

            if pressed: 
                s_result.hold_button()
            else:
                s_result.release_button()
                
                
        #sss.control(key_input_once)
        sss.move()
        sss.draw()
        
        # 単発押しキーの状態をすべてリセット
        for key in key_input_once.keys():
            key_input_once[key] = False


        pygame.display.update()
        
        # メインループここまで

if __name__ == "__main__":
    try:
        main()

    finally:
        pygame.quit()
        printer.close_serial()
        log_message(logger, message='System end')
        slack.post(":no_entry: システム終了\n")

        os._exit(-1) 
