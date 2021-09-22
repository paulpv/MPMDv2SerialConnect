#!/usr/bin/env python3
#
# https://pyserial.readthedocs.io/en/latest/pyserial_api.html
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python get-pip.py
# python -m pip install pyserial
# python -m serial.tools.miniterm COM7 115200
#

import argparse
import platform
import serial
import sys
import time

def get_serial(portName, baudrate=115200, read_timeout=2, hack=False):
  print(f'Opening {portName} {baudrate} N 8 1 to read')
  if hack:
    # https://plugins.octoprint.org/plugins/malyan_connection_fix/
    # https://github.com/OctoPrint/OctoPrint/issues/2271
    # https://github.com/OctoPrint/OctoPrint-MalyanConnectionFix
    # https://github.com/OctoPrint/OctoPrint-MalyanConnectionFix/blob/master/octoprint_malyan_connection_fix/__init__.py#L56
    serial_obj1 = serial.Serial(str(portName), baudrate, timeout=read_timeout, writeTimeout=10,
                                parity=serial.PARITY_ODD)
    serial_obj2 = serial.Serial(str(portName), baudrate, timeout=read_timeout, writeTimeout=10,
                              parity=serial.PARITY_NONE)
    serial_obj1.close()  # close the first instance, we don't actually need that
    return serial_obj2  # return the second instance
  else:
    ser = serial.Serial(baudrate=baudrate,
      bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
      timeout=read_timeout, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None,
      exclusive=None)
    ser.port = portName
    ser.open()
    return ser

def main():
  _system = platform.system()
  print(f'Platform: {_system}')
  defaultPortName = {
    'Windows':'COM7',
    'Darwin':'/dev/tty.usbserial-144230', # MacOS
  }.get(_system, '/dev/ttyUSB0') # Default assume Raspberry Pi

  parser = argparse.ArgumentParser(description='Read from serial port')
  parser.add_argument('portName', nargs='?', help='serial port to read from', default=defaultPortName)
  parser.add_argument('--hack', action='store_true', help='use Malyan double open hack', default=False)
  args = parser.parse_args()

  portName = args.portName
  print(f'portName={repr(portName)}')

  hack = args.hack
  print(f'hack={repr(hack)}')

  ser = get_serial(portName, hack=hack)

  if False:
    timeout = 5
    # ? https://github.com/pyserial/pyserial/issues/517#issuecomment-691797151
    print(f'#HACK experiment sleep {timeout} seconds before reading...')
    time.sleep(timeout)

  print('Reading...')
  seq = []
  while True:
    cs = ser.read(ser.in_waiting or 1)
    #print(cs)
    for c in cs:
      c = chr(c)
      if c == '\n':
        print(''.join(str(v) for v in seq))
        seq = []
      else:
        seq.append(c)
  ser.close()

if __name__ == "__main__":
  main()