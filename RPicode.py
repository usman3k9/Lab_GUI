import time
import socket
import struct
import threading
import RPi.GPIO as GPIO

BOARD_IP = "192.168.230.31"
RTIO_IP = "192.168.230.31"
_receivingPORT = 15000
_sendingPORT = 9200
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_UP)

class Board(object):
    def __init__(self,RTIO_IP,_sendingPORT):
        self.RTIO_IP                     = RTIO_IP
        self._sendingPORT                = _sendingPORT
        self._txSock                     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sw1_1=0;
        self.sw1_2=0;
        self.sw1_3=0;
        self.sw2_1=0;
        self.sw2_2=0;
        self.sw2_3=0;
        self.sw3_1=0;
        self.sw3_2=0;
        self.sw3_3=0;
        self.sw4_1=0;
        self.sw4_2=0;
        self.sw4_3=0;
        self.sw5_1=0;
        self.sw5_2=0;
        self.sw5_3=0;
        self.sw6_1=0;
        self.sw6_2=0;
        self.sw6_3=0;
        
    def Sender(self):
        var = struct.pack('18b',self.sw1_1,
                          self.sw1_2,
                          self.sw1_3,
                          self.sw2_1,
                          self.sw2_2,
                          self.sw2_3,
                          self.sw3_1,
                          self.sw3_2,
                          self.sw3_3,
                          self.sw4_1,
                          self.sw4_2,
                          self.sw4_3,
                          self.sw5_1,
                          self.sw5_2,
                          self.sw5_3,
                          self.sw6_1,
                          self.sw6_2,
                          self.sw6_3)
                          
        var = str.encode(str(GPIO.input(7)))                  
        self._txSock.sendto(var,(self.RTIO_IP,self._sendingPORT))                  
        #self._txSock.sendto(var,(self.RTIO_IP,self._sendingPORT))
        #time.sleep(0.1)
        
class BoardHandler(object):
    def __init__(self,boardProcessor):
        self.isHandling = True
        self.boardProcessor = boardProcessor
        self._txThread = threading.Thread(target=self.logicHandler)
        
    
    def logicHandler(self):
        while self.isHandling:
            self.boardProcessor.Sender()

            
    def startHandling(self):
        self._txThread.start()
        
    def stopHandling(self):
        self.isHandling = False

Board = Board(RTIO_IP,_sendingPORT)
BoardHandler = BoardHandler(Board)
BoardHandler.startHandling()

