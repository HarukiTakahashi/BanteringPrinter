import serial
from serial.tools import list_ports
import time, datetime
import threading

class Printer():
    COMMAND_BUFFER_MAX = 5
    event = threading.Event()

    def __init__(self):
        self.serial = serial.Serial()
        self.command_buffer = 0    
        self.serial.timeout = 1
        self.serial.write_timeout = 1

        self.serial.baudrate = "115200"
        self.stat = 0 # 現在の3Dプリンタの状態

        self.gcode = []
        
        self.isPrinting = False
        self.feedrate = 100

    def connect(self):
        ports = list_ports.comports()    # ポートデータを取得
        devices = [info.device for info in ports]
        print(ports)

        if len(devices) == 0:
            print("error: device not found")
            return None
        elif len(devices) == 1:
            print("only found %s" % devices[0])
            self.serial.port = devices[0]
        else:
            for i in range(len(devices)):
                print("input %3d: open %s" % (i,devices[i]))
            print("input number of target port >> ",end="")
            num = 0 #int(input())
            self.serial.port = devices[num]
    
        try:
            self.serial.open()
            print("serial open!")
            return self.serial
        except:
            print("error when opening serial")
            return None

    def printing(self):
        self.isPrinting = True

        for g in self.gcode:
            pos = g.find(";")
            if pos != -1:
                g = g[:pos]

            if len(g) == 0:
                continue

            self.serial_send(g)
        print("DONE")
        self.isPrinting = False
    
    def change_feedrate(self, per):
        print("===== change feedrate ===== ")
        g = "M220 S" + str(per)
        self.serial_force_send(g)
        
        self.feedrate = per
    
    def serial_read(self):
        while True:
            time.sleep(0.01)
                        
            try:
                data = self.serial.readline()
            except serial.SerialException as e:
                #There is no new data from serial port
                return None
            except TypeError as e:
                #Disconnect of USB->UART occured
                self.serial.port.close()
                return None
            

            if data != b'':
                ret = data.decode('utf-8')
                ret = ret.strip()
                print(datetime.datetime.now(), " <<< RECV ", ret)

                # 命令を処理し終えたら "ok" が返ってくる
                if ret.find("ok") != -1:
                    self.command_buffer -= 1
                    if self.command_buffer < 0:
                        self.command_buffer = 0

    def serial_force_send(self, data: str):
        data = bytes(data+ "\r\n", encoding = "utf-8")
        if data.decode('utf-8').find(";") == 0:
            print("comment!!!")
            return
        
        self.serial.write(data)
        print(datetime.datetime.now(), " SEND >>> ", data.decode('utf-8').strip())
 
    def serial_send(self, data: str):
        data = bytes(data+ "\r\n", encoding = "utf-8")
        
        if data.decode('utf-8').find(";") == 0:
            print("comment!!!")
            return
        
        start_time = time.time()

        while True:
            time.sleep(0.01)
            #print("buf",self.command_buffer)
            if self.command_buffer < Printer.COMMAND_BUFFER_MAX:
                self.command_buffer += 1
                
                self.serial.write(data)
                
                print(datetime.datetime.now(), " SEND >>> ", data.decode('utf-8').strip())
                return True
            if time.time() - start_time > 60:
                print("Time out")
                break

        return False


    def start_reading(self):
        self.thread = threading.Thread(target=self.serial_read)
        self.thread.start()

    def start_printing(self):
        self.thread = threading.Thread(target=self.printing)
        self.thread.start()


    def open_gcode_file(self, path):
        f = open(path, "r")
        self.gcode = f.readlines()
        
    def close_serial(self):
        g = "M84"
        self.serial_force_send(g)

        self.serial.close()
        print("serial closed")    
