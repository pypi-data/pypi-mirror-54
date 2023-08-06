#!/usr/bin/env python3

from __future__ import division, print_function

import serial
import os
import sys
import time
import struct
import argparse

import pyprind
from xmodem import XMODEM1k

__version__ = "1.1.0"

CMD_SET_BAUD = 0x31
CMD_ERASE    = 0x32 # ROM boot only
CMD_SET_SEC  = 0x33 # ROM boot only
CMD_GET_SEC  = 0x34 # ROM boot only
CMD_SET_GAIN = 0x35
CMD_GET_GAIN = 0x36
CMD_SET_MAC  = 0x37
CMD_GET_MAC  = 0x38
CMD_GET_QFID = 0x3c # ROM boot only
CMD_ERASE_SECBOOT = 0x3f

# CRC-16/CCITT-FALSE
def crc16(data : bytearray):
    crc = 0xFFFF
    for i in range(0, len(data)):
        crc ^= data[i] << 8
        for j in range(0,8):
            if (crc & 0x8000) > 0:
                crc =(crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF

def putc(c):
    sys.stdout.write(c)
    sys.stdout.flush()

def error_exit(msg):
    print('Error:', msg)
    sys.exit(1)

# ser = None

def deviceHardReset(self):
    self.setRTS(True)
    time.sleep(0.1)
    self.setRTS(False)

def deviceWaitBoot(self,timeout = 3):
    self.timeout = 0.01
    self.flushInput()
    started = time.time()
    buff = b''
    while time.time() - started < timeout:
        self.write(b'\x1B')
        buff = buff + self.read(1)
        buff = buff[-16:]            # Remember last 16 chars
        if buff.endswith(b'CCCC'):
            return True
    return False

def sendCommand(self,cmd):
    cmd = struct.pack('<BHH', 0x21, len(cmd)+2, crc16(cmd)) + cmd
    self.flushInput()
    self.write(cmd)
    self.flush()
    #print('<<< ', cmd.hex())

def deviceSetBaud(self,baud):
    prev_baud = self.baudrate
    
    def serialSetBaud(self,value):
        if self.baudrate == value:
            return
        self.close()
        self.baudrate = value
        self.open()
        time.sleep(0.1)

    for retry in range(3):
        serialSetBaud(self,prev_baud)
        sendCommand(self,struct.pack('<II', CMD_SET_BAUD, baud))
        serialSetBaud(self,baud)
        if deviceWaitBoot(self):
            return True
          
    serialSetBaud(self,prev_baud)
    return False

def deviceEraseImage(self):
    self.timeout = 1
    sendCommand(self,struct.pack('<I', CMD_ERASE))
    return deviceWaitBoot(self,5)

def deviceEraseSecboot(self):
    self.timeout = 1
    sendCommand(self,struct.pack('<I', CMD_ERASE_SECBOOT))
    deviceWaitBoot(self,15)
    return deviceIsInRomBoot(self)

def deviceIsInRomBoot(self):
    return (deviceGetFlashID(self) != None)

def deviceSetMAC(self,mac):
    self.timeout = 1
    sendCommand(self,struct.pack('<I', CMD_SET_MAC) + mac)

def deviceGetMAC(self):
    self.timeout = 1
    sendCommand(self,struct.pack('<I', CMD_GET_MAC))
    result = self.read_until(b'\n')
    result = result.decode('ascii').upper().strip()
    if result.startswith('MAC:'):
        return result[4:]
    return None

def deviceGetFlashID(self):
    self.timeout = 1
    sendCommand(self,struct.pack('<I', CMD_GET_QFID))
    result = self.read_until(b'\n')
    result = result.decode('ascii').upper().strip()
    if result.startswith('FID:'):
        return result[4:]
    return None

def deviceUploadFile(self,fn):
    self.timeout = 1
    statinfo_bin = os.stat(fn)
    bar = pyprind.ProgBar(statinfo_bin.st_size//1024)

    def ser_write(data, timeout=1):
        bar.update()
        return self.write(data)

    def ser_read(size, timeout=1):
        return self.read(size)

    stream = open(fn, 'rb+')
    time.sleep(0.2)
    modem = XMODEM1k(ser_read, ser_write)
    self.flushInput()
    if modem.send(stream):
        time.sleep(1)
        reply = self.read_until(b'run user code...')
        reply = reply.decode('ascii').strip()
        return reply

    return None
  
import serial.tools.list_ports

def getDefaultPort():
    comlist = serial.tools.list_ports.comports()
    if comlist:
        return comlist[0].device;

    if platform.system() == 'Windows':
        return "COM1"
    else:
        return "/dev/ttyUSB0"

def main():

    supportedBauds = [115200, 460800, 921600, 1000000, 2000000]

    parser = argparse.ArgumentParser(prog='w600tool')
    parser.add_argument('-p', '--port',   default=getDefaultPort())
    parser.add_argument('-b', '--baud',   default=115200,  type=int, choices=supportedBauds, metavar='BAUD')
    parser.add_argument('--get-mac',      action="store_true")
    parser.add_argument('--set-mac',      metavar='MAC')
    parser.add_argument('--erase', '-e',  action="store_true")
    parser.add_argument('--upload', '-u', metavar='FILE')
    parser.add_argument('--upload-baud',  default=2000000, type=int, choices=supportedBauds)
    parser.add_argument('--version',      action='version', version='%(prog)s '+ __version__)
    args = parser.parse_args()

    print('Opening device:', args.port)
    ser = serial.Serial(args.port, args.baud, timeout=1)

    deviceHardReset(ser)
    if not deviceWaitBoot(ser):
        print('Push reset button to enter bootloader...')
        if not deviceWaitBoot(ser,15):
            error_exit('Bootloader not responding')

    if args.set_mac:
        mac = args.set_mac.replace(':','').replace(' ','').upper()
        print('Setting MAC:', mac)
        deviceSetMAC(ser,bytearray.fromhex(mac))

    if args.get_mac:
        mac = deviceGetMAC(ser)
        print('MAC:', mac)

    if args.erase:
        print('Erasing secboot')
        if not deviceEraseSecboot(ser):
            error_exit('Erasing secboot failed')

        print('Erasing image')
        deviceEraseImage(ser)
        deviceWaitBoot(ser,5)

    if args.upload:
        if not os.path.exists(args.upload):
            error_exit('The specified file does not exist')
            
        _, ext = os.path.splitext(args.upload)
        ext = ext.lower()

        if ext == '.fls' and not args.erase:
            print('Erasing secboot')
            if not deviceEraseSecboot(ser):
                error_exit('Erasing secboot failed => Try entering ROM boot manually')
        elif ext == '.img' and deviceIsInRomBoot(ser):
            error_exit('ROM bootloader only accepts FLS files')

        if args.upload_baud != ser.baudrate:
            if deviceSetBaud(ser,args.upload_baud):
                print('Switched speed to', ser.baudrate)
            else:
                print('Warning: Cannot switch speed')
                if not deviceWaitBoot(ser,5):
                    error_exit('Could not recover from speed switch failure => Try again, or set upload-baud to 115200')

        print('Uploading', args.upload)
        reply = deviceUploadFile(ser,args.upload)
        
        print("Reset board to run user code...")
        deviceHardReset(ser) #reset device


def _main():
    main()


if __name__ == '__main__':
    _main()



