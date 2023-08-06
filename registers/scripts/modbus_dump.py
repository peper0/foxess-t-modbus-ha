# ssh -L 8234:192.168.10.31:8234 pi@burak.local
# ssh -L 8234:USR-TCP232-304:8234 pi@burak.local
import datetime
import logging
import time
from contextlib import suppress

import pymodbus
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.framer.rtu_framer import ModbusRtuFramer
from pymodbus.other_message import GetCommEventCounterRequest, ReadExceptionStatusRequest
from pymodbus.register_read_message import ReadInputRegistersResponse, ReadRegistersResponseBase
import pickle

# client = ModbusSerialClient("rtu")
HOST = '127.0.0.1'
PORT = 8234
UNIT_ID = 1

client: ModbusTcpClient = None


def reconnect():
    global client
    if client:
        client.close()
    client = ModbusTcpClient(HOST, port=PORT, framer=ModbusRtuFramer)
    client.connect()


reconnect()

def read_reg(reg, count) -> ReadRegistersResponseBase:
    while True:
        with suppress():
            r = client.read_input_registers(reg, count, unit=UNIT_ID)
        if isinstance(r, ModbusIOException):
            print("reconnect")
            reconnect()
        elif isinstance(r, ReadRegistersResponseBase):
            return r
        print("error: ", r)

INPUT_REGS = [
    (10000, 1),
    (10020, 16),
    (10032, 16),
    (10052, 3),
    (10055, 3),
    (10058, 3),
    (10061, 3),
    (10064, 3),
    (10100, 24),
    # (10500, 10),
    (10500, 20),
    # 3: changes from 2 to 3, 4
    # 7: power [W] (rest const)
    (10504, 2),
    (10692, 1),
    (10693, 1),
    (10694, 1),
    (10695, 1),
    (10696, 1),
    (10697, 1),
    (10698, 1),
    (10699, 1),
    # (10700, 4),
    (10700, 20),
    # [0] R Voltage 0.1 V
    # [1] R Current 0.1 A
    # [2] R Freq 0.01 Hz
    # [3] R Power [W]
    # (10800, 12),
    (10800, 20),
    # [0]: np. 4241 i się zmienia
    (11200, 3),
    # Inv or boost
    # Inv or boost
    # Ambient
    (11300, 20),
    (11500, 20),
    # (11800, 16),
    (11800, 20),
    (12800, 3),
    # year
    # ?
    # minutes?
]

# read data and save to file
data = []

with open("data", "rb") as f:
    data = pickle.load(f)

while True:
    record = dict()
    record[0] = datetime.datetime.now()
    for reg, count in INPUT_REGS:
        r = read_reg(reg, count)
        record[reg] = r.registers
        time.sleep(0.1)
    data.append(record)
    print(record)
    time.sleep(1)

    with open("data", "wb") as f:
        pickle.dump(data, f)

# monitor a single register
REG = 10500
COUNT = 20
FIELD = 7
while True:
    r = read_reg(REG, COUNT)
    print(r.registers[FIELD])
    time.sleep(1)
