import time
import datetime
import os
import glob
import sys

try:
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
          temp_f = temp_c * 9.0 / 5.0 + 32.0
          print datetime.datetime.now(),"Current Temperature is: %.2f" %read_temp(),"C %.2f" %temp_f,"F"
	  time.sleep(1)
except:
  print '=================== error ================='
finally:
  print '=================== stop =================='
  sys.exit(1)
