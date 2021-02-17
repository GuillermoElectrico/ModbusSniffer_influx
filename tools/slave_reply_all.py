import serial
from pymodbus.factory import ClientDecoder
from pymodbus.factory import ServerDecoder
#import pymodbus
#from pymodbus.transaction import ModbusRtuFramer
#from pymodbus.utilities import hexlify_packets
#from binascii import b2a_hex
from time import sleep
import sys
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer
#from custom_message import CustomModbusRequest
#import socat_test as socat
from pymodbus.server.sync import StartSerialServer
from modbus_sniffer import SerialSnooper
#asynchronous import StartSerialServer
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
#log.setLevel(logging.DEBUG)
#log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)
import copy

def run_server(device, baud=9600):
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [25185]*1024),
        ir=ModbusSequentialDataBlock(0, [25185]*1024))
    slaves = {1 : copy.deepcopy(store),
              2 : copy.deepcopy(store),
              3 : copy.deepcopy(store),
              4 : copy.deepcopy(store),
              5 : copy.deepcopy(store),
              6 : copy.deepcopy(store),
              246 : copy.deepcopy(store)}
    context = ModbusServerContext(
        slaves=slaves,
        single=False,
    )

    # RTU Server
    StartSerialServer(
        context,
        identity=None,
        port=device,
        timeout=3.5*10/baud,
        framer=ModbusRtuFramer,
        stopbits=1,
        bytesize=8,
        parity=serial.PARITY_NONE,
        baudrate=baud)

if __name__ == "__main__":
    baud = 9600
    try:
        port = sys.argv[1]
    except IndexError:
        print("Usage: python3 {} device [baudrate, default={}]".format(sys.argv[0], baud))
        sys.exit(-1)
    try:
        baud = int(sys.argv[2])
    except (IndexError,ValueError):
        pass

    run_server(device=port, baud=baud)


