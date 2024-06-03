import serial
import re
from serial.tools import list_ports
import time, datetime
import threading

class Printer():
    COMMAND_BUFFER_MAX = 5
    DEFAULT_FEEDRATE = 100
    event = threading.Event()

    def __init__(self):
        self.serial = serial.Serial()
        self.command_buffer = 0    
        self.serial.timeout = 1
        self.serial.write_timeout = 1

        self.serial.baudrate = "115200"
        self.stat = 0 # 現在の3Dプリンタの状態

        self.gcode_file_name = None # 造形対象のGcodeファイル名
        self.gcode = [] # 造形対象のGcode
        self.gcode_printing = [] # 造形中のGcode
        self.gcode_len = -1
        self.nozzle_temp = -1
        self.bed_temp = -1       
        
        self.is_printing = False
        self.is_waiting = False
        self.enable_check_temp = False
        self.feedrate = 100

    # 造形プロセス制御 ================================
    # 接続失敗の場合はNoneが返る
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

    # 造形プロセス制御 ================================
    def printing(self):
        self.is_printing = True
        
        self.gcode_printing = list(self.gcode)
        self.gcode_len = len(self.gcode_printing)

        # リストを一度コピーしてそこから順番に取り出す処理に
        while len(self.gcode_printing) > 0:
            g = self.gcode_printing.pop(0)
            self.serial_send(g.strip())

#        for g in self.gcode:
#            self.serial_send(g.strip())
#            time.sleep(0.001)
            
        print("DONE")
        self.command_buffer = 0
        self.feedrate = Printer.DEFAULT_FEEDRATE
        self.change_feedrate(self.feedrate)
        self.is_printing = False
    
    # feedrateの変更 ================================
    def change_feedrate(self, per):
        if self.is_waiting:
            print("WAITING!!!")
            return    
        
        print("===== change feedrate ===== ")
        g = "M220 S" + str(per)
        
        # self.serial_force_send(g)
        
        if self.is_printing:            
            # 造形中ならリストに追加
            self.gcode_printing.insert(1, g)

        else:
            # そうでないなら強制送信
            self.serial_force_send(g)

        self.feedrate = per
        time.sleep(0.01) # いるかな？
            
    
    # シリアル読み込み ================================
    def serial_read(self):
        while True:
            time.sleep(0.001)
            #print("BUF NUM : " + str(self.command_buffer))
                        
            try:
                data = self.serial.readline()
            except serial.SerialException as e:
                # There is no new data from serial port
                #return None
                pass
            except TypeError as e:
                # Disconnect of USB->UART occured
                # self.serial.port.close()
                #return None
                pass
            
            if data != b'':
                ret = data.decode('utf-8')
                ret = ret.strip()
                print(datetime.datetime.now(), " <<< RECV ", ret)

                # 温度設定
                if ret.find("T:") != -1 and ret.find("B:") != -1:
                    pattern = r'T:([^ ]*)|B:([^ ]*)'
                    matches  = re.findall(pattern, ret)
                    results = [match[0] if match[0] else match[1] for match in matches]
                    self.nozzle_temp = float(results[0])
                    self.bed_temp = float(results[1])

                # 命令を処理し終えたら "ok" が返ってくる
                if ret.find("ok") != -1:
                    self.is_waiting = False
                    self.command_buffer -= 1
                    if self.command_buffer < 0:
                        self.command_buffer = 0

     # シリアル強制送信 ================================
    def serial_force_send(self, data: str):
        if self.is_waiting:
            print("WAITING!!!")
            return
    
        data = data.strip()
        if len(data) == 0:
            return
        if data.find(";") == 0:
            return
        pos = data.find(";")
        if pos != -1:
            data = data[:pos]
        data = bytes(data+ "\r\n", encoding = "utf-8")
        if data.decode('utf-8').find(";") == 0:
            print("comment!!!")
            return
        
        try:
            self.serial.write(data)
        except serial.SerialException as e:
            #There is no new data from serial port
            print("E - serial.SerialException when forcely sending")
            return None
        except TypeError as e:
            #Disconnect of USB->UART occured
            print("E - Type error when forcely sending")
            #self.serial.port.close()
            return None

        self.command_buffer += 1
        print(datetime.datetime.now(), " SEND >>> ", data.decode('utf-8').strip())
 
     # シリアル送信 ================================
    def serial_send(self, data: str):
        data = data.strip()
        if len(data) == 0:
            return
        if data.find(";") == 0:
            return
        pos = data.find(";")
        if pos != -1:
            data = data[:pos]

        # todo : M109, M190のときはストップ
        data = bytes(data+ "\r\n", encoding = "utf-8")
    
        start_time = time.time()
        while True:
            time.sleep(0.01)
            #print("buf",self.command_buffer)
            if self.is_waiting:
                continue

            if self.command_buffer < Printer.COMMAND_BUFFER_MAX:
                self.command_buffer += 1
                
                if data.decode('utf-8').find("M109") != -1 or data.decode('utf-8').find("M190") != -1:
                    self.is_waiting = True
                    
                try:
                    self.serial.write(data)
                except serial.SerialException as e:
                    #There is no new data from serial port
                    print("E - serial.SerialException when sending")
                    #return None
                    continue
                except TypeError as e:
                    #Disconnect of USB->UART occured
                    print("E - Type error when sending")
                    #self.serial.port.close()
                    #return None
                    continue
                
                print(datetime.datetime.now(),   " SEND >>> ", data.decode('utf-8').strip())
                
                return True
            
            if time.time() - start_time > 100:
                print("Time out")
                self.command_buffer -= 1
                print(data.decode('utf-8'))
                break
    
        return False

    def check_temperature(self):
        while True:
            time.sleep(1)
            if self.enable_check_temp:

                g = "M105"
                if self.is_printing:   
                    # 造形中ならリストに追加
                    self.gcode_printing.insert(1, g)
                else:
                    # そうでないなら強制送信
                    self.serial_force_send(g)

    def control_speed(self):
        while True:
            time.sleep(1)

            if self.feedrate > 50:
                self.feedrate -= 1

            g = "M220 S" + str(self.feedrate)
            if self.is_printing:   
                # 造形中ならリストに追加
                self.gcode_printing.insert(1, g)
            else:
                # そうでないなら強制送信
                self.serial_force_send(g)
        


    def start_reading(self):
        self.thread_read = threading.Thread(target=self.serial_read)
        self.thread_read.start()

    def start_printing(self):
        self.thread_print = threading.Thread(target=self.printing)
        self.thread_print.start()

    def start_checking_temp(self):
        self.thread_temp = threading.Thread(target=self.check_temperature)
        self.thread_temp.start()

    def start_controlling_speed(self):
        self.cont_speed = threading.Thread(target=self.control_speed)
        self.cont_speed.start()

    def open_gcode_file(self, path):
        f = open(path, "r")
        self.gcode = f.readlines()
        
    def close_serial(self):
        g = "M84"
        self.serial_force_send(g)

        self.serial.close()
        print("serial closed")    


    def get_progress(self):
        return len(self.gcode_printing), self.gcode_len