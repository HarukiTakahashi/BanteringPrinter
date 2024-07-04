from functools import partial
import time

import nfc
from typing import cast

class Card(object):

    def __init__(self):
        self.clf = None
        self.on_card = False

    def on_connect(self, tag):
        self.on_card = True
        if tag != None:
            
            try:
                tag.dump()

                servc = 0x1A8B
                service_code = [nfc.tag.tt3.ServiceCode(servc >> 6, servc & 0x3F)]
                bc_id = [nfc.tag.tt3.BlockCode(0)]
                bd_id = cast(bytearray, tag.read_without_encryption(service_code,bc_id))
                
                self.id_info = bd_id.decode('utf-8')
                self.id_info = self.id_info.replace('\x00', '')
                self.id_info = self.id_info[2:-2]
                self.id_str = self.id_info 

                print(self.id_str)
        
            except:
                print("Error")
                pass

        return True

    def on_release(self, tag):
        print("release")
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

    def __call__(self, started, n):

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

card=Card()
while True:
    print("!")
    time.sleep(1)
    card(time.time(), 1)
    

print("done")