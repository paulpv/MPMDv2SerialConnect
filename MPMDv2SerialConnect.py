#
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python get-pip.py
# python -m pip install pyserial
# python -m serial.tools.miniterm COM8 115200
#

import serial
import time

#portName = 'COM8'
portName = '/dev/tty.usbserial-144230'
ser = serial.Serial(baudrate=115200,
  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
  timeout=2, xonxoff=True, rtscts=True, write_timeout=None, dsrdtr=True, inter_byte_timeout=None,
  exclusive=None)
ser.port = portName
print('Opening COM7 115200 N 8 1 to read')
ser.open()

if False:
  # ? https://github.com/pyserial/pyserial/issues/517#issuecomment-691797151
  print('#HACK experiment sleep 5 seconds before reading...')
  time.sleep(5)
print('Reading...')
seq = []
count = 1
while True:
  for c in ser.read(ser.in_waiting or 1):
    c = chr(c)
    if c == '\n':
      print(''.join(str(v) for v in seq))
      seq = []
    else:
      seq.append(c)
ser.close()
