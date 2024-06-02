import nfc
import threading
import time

class NFCReading():
    
    def __init__(self):
        self.id_info = ""

    def on_connect(self, tag: nfc.tag.Tag) -> bool:
        if tag != None:
            
            try:
                print("connected")
                tag.dump()

                servc = 0x1A8B
                service_code = [nfc.tag.tt3.ServiceCode(servc >> 6, servc & 0x3F)]
                bc_id = [nfc.tag.tt3.BlockCode(0)]
                bd_id = tag.read_without_encryption(service_code,bc_id)
                bd_id = bd_id.decode("utf-8")
                
                self.id_info = bd_id[2:-2]

            except:
                print("Error")
                pass

        return True  # Trueを返しておくとタグが存在しなくなるまで待機され、離すとon_releaseが発火する


    def on_release(self, tag: nfc.tag.Tag) -> None:
        print("released")
        self.id_info = ""

    def start_reading(self):
        self.thread_nfc_read = threading.Thread(target=self.reading)
        self.thread_nfc_read.start()

    def reading(self):
        clf = nfc.ContactlessFrontend("usb")
        while True:
            time.sleep(0.1)
            clf.connect(rdwr={"on-connect": self.on_connect, "on-release": self.on_release})

    def get_nfc_id(self):
        self.id_info = self.id_info.replace("\n","")
        return str(self.id_info)