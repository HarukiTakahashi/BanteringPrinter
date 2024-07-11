import nfc
import threading
import time
from functools import partial
from typing import cast
import pygame
from pygame.locals import *


class NFCReading():
    
    def __init__(self):
        self.on_card = False
        self.id_info = ""
        self.id_str = "Anonymous user"
        self.clf = None
    
    # 言語設定
    def set_lang(self, i: int):
        self.lang = i

        if self.lang == 0:
            self.id_str = "匿名ユーザ"
        elif self.lang == 1:
            self.id_str = "Anonymous user"

    def set_fx_pikon(self, s):
        self.pikon = s

    def set_fx_bubu(self, s):
        self.bubu = s

    def on_connect(self, tag: nfc.tag.Tag) -> bool:
        self.on_card = True
        if tag != None:
            
            try:
                print("connected")
                tag.dump()

                servc = 0x1A8B
                service_code = [nfc.tag.tt3.ServiceCode(servc >> 6, servc & 0x3F)]
                bc_id = [nfc.tag.tt3.BlockCode(0)]
                bd_id = cast(bytearray, tag.read_without_encryption(service_code,bc_id))
                
                self.id_info = bd_id.decode('utf-8')
                self.id_info = self.id_info.replace('\x00', '')
                self.id_info = self.id_info[2:-2]
                self.id_str = self.id_info 
                self.pikon.play()

            except:
                print("Error")
                self.bubu.play()
                pass

        return True  # Trueを返しておくとタグが存在しなくなるまで待機され、離すとon_releaseが発火する

    def on_release(self, tag: nfc.tag.Tag) -> None:
        print("released")
        self.id_info = ""
        if self.lang == 0:
            self.id_str = "匿名ユーザ"
        elif self.lang == 1:
            self.id_str = "Anonymous user"
    
        self.on_card = False
        return True
    
    def after(self, started, n):
        return time.time() - started > n and not self.on_card

    def connect(self):
        while True:
            try:
                self.clf = nfc.ContactlessFrontend('usb')
                print("NFCリーダーに接続しました。")
                break
            except IOError:
                print("NFCリーダーに接続できませんでした。再試行します...")
                time.sleep(1)  # 1秒待ってから再試行
      
    def get_nfc_id(self):
        self.id_info = self.id_info.replace("\n","")
        return str(self.id_info)
    

        
    def read(self, started, n):
        self.connect()

        try:
            self.clf.connect(
                rdwr = {
                    'on-connect': self.on_connect,
                    'on-release': self.on_release
                },
                terminate=partial(self.after, started, n)
                )

        except IOError as e:
            print("リーダーが接続されていません")
            self.clf.close()
            self.clf = None
        
        self.clf.close()
        self.clf = None

    def start_reading(self):
        self.thread_nfc_read = threading.Thread(target=self.reading)
        self.thread_nfc_read.start()

    def reading(self):
        while True:
            time.sleep(1)
            self.read(time.time(), 1)

"""
class NFCReading():
    
    def __init__(self):
        self.id_info = ""
        self.id_str = "Anonymous user"
        self.clf = None

    def on_connect(self, tag: nfc.tag.Tag) -> bool:
        if tag != None:
            
            try:
                print("connected")
                tag.dump()

                servc = 0x1A8B
                service_code = [nfc.tag.tt3.ServiceCode(servc >> 6, servc & 0x3F)]
                bc_id = [nfc.tag.tt3.BlockCode(0)]
                bd_id = cast(bytearray, tag.read_without_encryption(service_code,bc_id))
                
                self.id_info = bd_id.decode('utf-8')
                self.id_info = self.id_info.replace('\x00', '')
                self.id_info = self.id_info[2:-2]
                self.id_str = self.id_info 

            except:
                print("Error")
                pass

        return True  # Trueを返しておくとタグが存在しなくなるまで待機され、離すとon_releaseが発火する

    def on_release(self, tag: nfc.tag.Tag) -> None:
        print("released")
        self.id_info = ""
        self.id_str = "Anonymous user"

    def start_reading(self):
        self.thread_nfc_read = threading.Thread(target=self.reading)
        self.thread_nfc_read.start()

    def reading(self):
        self.clf = nfc.ContactlessFrontend("usb")
        while True:
            time.sleep(0.1)
            self.clf.connect(rdwr={"on-connect": self.on_connect, "on-release": self.on_release})
            
    def get_nfc_id(self):
        self.id_info = self.id_info.replace("\n","")
        return str(self.id_info)
    
    def close_nfc(self):
        pass
        
"""