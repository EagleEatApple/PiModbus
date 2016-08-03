import time
import datetime
import os
import glob
import sys
import modbus_tk
import modbus_tk.defines as mdef
import modbus_tk.modbus
import modbus_tk.modbus_tcp
import struct 


try:

  server = modbus_tk.modbus_tcp.TcpServer(port=502, address='127.0.0.1', timeout_in_sec=3)
  server.start()
  slave_1 = server.add_slave(1)
  slave_1.add_block('slave1_block1', mdef.HOLDING_REGISTERS, 300, 100)
  slave_1.add_block('slave2_block1', mdef.HOLDING_REGISTERS, 400, 100)

  os.system('modprobe w1-gpio')
  os.system('modprobe w1-therm')
 
  base_dir = '/sys/bus/w1/devices/'
  device_folder = glob.glob(base_dir + '28*')[0]
  device_file = device_folder + '/w1_slave'
 
  def read_temp_raw():
      f = open(device_file, 'r')
      lines = f.readlines()
      f.close()
      return lines
 
  def read_temp():
      lines = read_temp_raw()
      while lines[0].strip()[-3:] != 'YES':
          time.sleep(0.2)
          lines = read_temp_raw()
      equals_pos = lines[1].find('t=')
      if equals_pos != -1:
          temp_string = lines[1][equals_pos+2:]
          return float(temp_string) / 1000.0
          
  while True:
	  temp_c = read_temp()
	  bytetemp = struct.unpack('HH',struct.pack('f',temp_c))
          temp_f = temp_c * 9.0 / 5.0 + 32.0
 	  slave_1.set_values('slave1_block1', 300, bytetemp)
          slave_1.set_values('slave2_block1', 400, temp_f)
          print datetime.datetime.now(),"Current Temperature is: %.2f" %read_temp(),"C %.2f" %temp_f,"F"
	  time.sleep(1)
except:
  print '=================== error ================='
finally:
  print '=================== stop =================='
  server.stop()
  sys.exit(1)
