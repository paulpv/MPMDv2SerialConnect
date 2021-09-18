#
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python get-pip.py
# python -m pip install pyserial
# python -m serial.tools.miniterm COM7 115200
#

import os
import serial
import time

print(f'OS: {os.name}')
if os.name == 'nt':
  portName = 'COM7'
else:
  portName = '/dev/tty.usbserial-144230'
ser = serial.Serial(baudrate=115200,
  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
  timeout=2, xonxoff=True, rtscts=True, write_timeout=None, dsrdtr=True, inter_byte_timeout=None,
  exclusive=None)
ser.port = portName
print(f'Opening {portName} 115200 N 8 1 to read')
ser.open()

if False:
  # ? https://github.com/pyserial/pyserial/issues/517#issuecomment-691797151
  print('#HACK experiment sleep 5 seconds before reading...')
  time.sleep(5)
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
