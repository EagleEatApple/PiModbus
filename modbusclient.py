import time
import modbus_tk
import modbus_tk.defines as mdef
import modbus_tk.modbus
import modbus_tk.modbus_tcp
import struct

try:
  while 1:
    time.sleep(1)
    master = modbus_tk.modbus_tcp.TcpMaster('127.0.0.1', 502)
    master.set_timeout(3)
    temperature = master.execute(1, mdef.HOLDING_REGISTERS, 300, 2)
    #print temperature[0],temperature[1]
    temp1 = struct.unpack('f',struct.pack('HH',temperature[0],temperature[1]))
    print 'Current temperature is %.2f' %temp1[0], 'C'
    #print 'Current temperature is 1', temperature[1], 'C'
    
except Exception as e:
    print '================================================= error ======================================================='
    print e
finally:
    print '================================================= stop ========================================================'
