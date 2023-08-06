# This script is mainly to disvover the modbus registers of the inverter.

# ssh -L 8234:192.168.10.31:8234 pi@burak.local

import logging
import time

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.framer.rtu_framer import ModbusRtuFramer
from pymodbus.other_message import GetCommEventCounterRequest, ReadExceptionStatusRequest
from pymodbus.register_read_message import ReadInputRegistersResponse, ReadRegistersResponseBase

# client = ModbusSerialClient("rtu")

client: ModbusTcpClient = None
i = 0
f = False


def reconnect():
    global client
    if client:
        client.close()
    client = ModbusTcpClient('127.0.0.1', port=8234, framer=ModbusRtuFramer)


reconnect()

if f:
    logging.getLogger('pymodbus').setLevel(logging.DEBUG)
    logging.getLogger('pymodbus.client.sync').setLevel(logging.DEBUG)
    logging.getLogger('pymodbus.transaction').setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    client.set_debug(True)
client.connect()

if f:
    client.execute(ReadExceptionStatusRequest())
    client.execute(GetCommEventCounterRequest())

    r = client.read_input_registers(10000, 1, unit=1)
    r = client.read_input_registers(10000, 2, unit=1)
    r.registers
    print(r)
    print(client.read_input_registers(10020, 6, unit=1))

    print(client.read_holding_registers(50200, 2, unit=1))
    if isinstance(r, ReadInputRegistersResponse):
        print(f"{i}: {r.registers}")
    # print(client.read_holding_registers(50100, 2, unit=1))
    # print(client.read_coils(50200, 2, unit=1))

    # read grid stats
    for i in range(100):
        r = client.read_input_registers(10700, 20, unit=1)
        if isinstance(r, ReadRegistersResponseBase):
            print(r.registers)
        time.sleep(1)

    # read pv power stats (no voltage or current)
    for i in range(100):
        r = client.read_input_registers(10500, 20, unit=1)
        if isinstance(r, ReadRegistersResponseBase):
            print(r.registers)
        time.sleep(1)

    # read pv  stats
    for i in range(100):
        r = client.read_input_registers(10800, 20, unit=1)
        if isinstance(r, ReadRegistersResponseBase):
            print(r.registers)
        time.sleep(1)

    # temperatures (inv, boost, ambient)
    for i in range(100):
        r = client.read_input_registers(11200, 3, unit=1)
        if isinstance(r, ReadRegistersResponseBase):
            print(r.registers)
        time.sleep(1)



for cnt in [3, 4, 5, 6]:
    i = 50000
    while i < 55000:
        if i % 1000 == 0:
            print(i)
        r = client.read_holding_registers(i, cnt, unit=1)
        if isinstance(r, ModbusIOException):
            print(i, "reconnecting")
            reconnect()
            i -= 1
        elif isinstance(r, ReadRegistersResponseBase):
            print(f"{i},{cnt}: {r.registers}")
        else:
            if r.exception_code != 2:
                print(i, r.original_code, r.exception_code, r)
        i += 1

# for cnt in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
for i in [
    50200,
    50201,
    50606,
    50621,
    50623,
    50800,
    50900,
    51100,
    51300,
    51500,
    51600,
    51700,
    51800,
    51900,
    52100,
    52200]:
    for cnt in range(24):
        r = client.read_holding_registers(i, cnt, unit=1)
        if isinstance(r, ModbusIOException):
            reconnect()
        elif isinstance(r, ReadRegistersResponseBase):
            print(f"{i},{cnt}: {r.registers}")

for i in [
    10000,
    10020,
    10032,
    10052,
    10055,
    10058,
    10061,
    10064,
    10100,
    10140,
    10500,
    10504,
    10692,
    10693,
    10694,
    10695,
    10696,
    10697,
    10698,
    10699,
    10700,
    10800,
    11200,
    11300,
    11500,
    11800,
    12000,
    12800,
]:
    for cnt in range(24, 34):
        r = client.read_input_registers(i, cnt, unit=1)
        if isinstance(r, ModbusIOException):
            reconnect()
        elif isinstance(r, ReadRegistersResponseBase):
            print(f"{i},{cnt}: {r.registers}")

i = 10000
while i < 12900:
    if i % 1000 == 0:
        print(i)
    r = client.read_input_registers(i, 4, unit=1)
    if isinstance(r, ModbusIOException):
        print(i, "reconnecting")
        reconnect()
        i -= 1
    elif isinstance(r, ReadInputRegistersResponse):
        print(f"{i}: {r.registers}")
    else:
        if r.exception_code != 2:
            print(i, r.original_code, r.exception_code, r)
    i += 1

# for i in range(0, 0x10000, 0x10):
for i in range(57984, 0x10000, 0x10):
    r = client.read_holding_registers(i, 1)
    print(i, r)

client.close()

for i in range(57984, 0x10000, 0x10):
    r = client.read_holding_registers(i, 1)
    print(i, r)

for i in range(0, 0x10000, 0x40):
    r = client.read_input_registers(i, 1)
    print(i, r)

for i in [10000, 10692, 10693, 10694, 10695, 10696, 10697, 10698, 10699]:
    r = client.read_input_registers(i, 1, unit=1)
    if isinstance(r, ModbusIOException):
        print(i, r)
    elif isinstance(r, ReadInputRegistersResponse):
        print(f"{i}: {r.registers}")
    else:
        if r.exception_code != 2:
            print(i, r.original_code, r.exception_code, r)

for i in range(100):
    time.sleep(1)
    print(client.read_input_registers(10698, 1, unit=1).registers)

# 50200
# 50201
# 50606
# 50621
# 50623
# 50800
# 50900
# 51600
"""
read_holding_registers 0-55000
50201,1: [14]
50606,1: [0]
50621,1: [1]
50623,1: [0]
50800,12: [60, 1000, 60, 100, 2530, 1955, 5010, 4950, 2530, 1955, 5020, 4950]
51300,8: [1, 5020, 400, 5010, 5010, 30, 90, 100]
51800,5: [1, 100, 0, 6000, 50]
51900,5: [0, 2500, 53, 0, 167]
51700,6: [0, 160, 60, 900, 8, 0]
52100,4: [2022, 1284, 4370, 4096]
52200,3: [4, 1, 2]
51300,10: [1, 5020, 400, 5010, 5010, 30, 90, 100, 0, 0]
51700,10: [0, 160, 60, 900, 8, 0, 0, 0, 0, 0]
51800,10: [1, 100, 0, 6000, 50, 0, 0, 0, 0, 0]
51900,10: [0, 2500, 53, 0, 167, 0, 0, 0, 0, 0]
52200,10: [4, 1, 2, 0, 0, 0, 0, 0, 0, 0]

cnt=2
50200 3 6 Exception Response(131, 3, SlaveBusy)
50201 3 6 Exception Response(131, 3, SlaveBusy)
50606 3 6 Exception Response(131, 3, SlaveBusy)
50621 3 6 Exception Response(131, 3, SlaveBusy)
50623 3 6 Exception Response(131, 3, SlaveBusy)
50800 3 6 Exception Response(131, 3, SlaveBusy)
50900 3 6 Exception Response(131, 3, SlaveBusy)
51100 3 6 Exception Response(131, 3, SlaveBusy)
51300 3 6 Exception Response(131, 3, SlaveBusy)
51500 3 6 Exception Response(131, 3, SlaveBusy)
51600 3 6 Exception Response(131, 3, SlaveBusy)
51700 3 6 Exception Response(131, 3, SlaveBusy)
51800 3 6 Exception Response(131, 3, SlaveBusy)
51900 3 6 Exception Response(131, 3, SlaveBusy)
52100 3 6 Exception Response(131, 3, SlaveBusy)
52200 3 6 Exception Response(131, 3, SlaveBusy)
"""

"""
read_input_registers 10000-12900
10692,1: [3]
10693,1: [12266]
10694,1: [1199]
10695,1: [0]
10696,1: [0]
10697,1: [0]
10698,1: [6550]
10699,1: [0]
10700,4: [2347, 5, 5000, 0]

10000,1: [4]
10020,16: [21558, 32, 8224, 8224, 8224, 8224, 8224, 8224, 8224, 8224, 8224, 8224, 8224, 8224, 8224, 8224]
10032,16: [13878, 12884, 13872, 12848, 12596, 18242, 12343, 13568, 0, 0, 0, 0, 0, 0, 0, 0]
10052,3: [16945, 12337, 12336]
10055,3: [13102, 13109, 0]
10058,3: [13102, 12337, 0]
10061,3: [13102, 12592, 0]
10064,3: [12590, 12336, 0]
10100,24: [57344, 0, 0, 0, 0, 0, 0, 0, 49910, 8, 16, 352, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
10500,10: [2, 0, 0, 48, 0, 2919, 0, 1095, 0, 0]
10500,20: [2, 0, 0, 48, 0, 2919, 0, 1093, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
10504,2: [0, 2919]
10692,1: [3]
10693,1: [12254]
10694,1: [1192]
10695,1: [0]
10696,1: [0]
10697,1: [0]
10698,1: [6579]
10699,1: [0]
10700,4: [2443, 16, 4997, 1151]
10700,20: [2447, 16, 4997, 1167, 2498, 16, 4997, 1167, 2362, 16, 4997, 1167, 0, 0, 0, 0, 0, 0, 0, 0]
10800,12: [3994, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
10800,20: [4012, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
11200,3: [24, 24, 31]
11300,20: [0, 29194, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6]
11500,20: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
11800,16: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
11800,20: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
12800,3: [2022, 1284, 4379]

count=2
10000 4 6 Exception Response(132, 4, SlaveBusy)
10100 4 6 Exception Response(132, 4, SlaveBusy)
10500 4 6 Exception Response(132, 4, SlaveBusy)
10700 4 6 Exception Response(132, 4, SlaveBusy)
10800 4 6 Exception Response(132, 4, SlaveBusy)
11200 4 6 Exception Response(132, 4, SlaveBusy)
11300 4 6 Exception Response(132, 4, SlaveBusy)
11500 4 6 Exception Response(132, 4, SlaveBusy)
11800 4 6 Exception Response(132, 4, SlaveBusy)
12000 4 6 Exception Response(132, 4, SlaveBusy)
12800 4 6 Exception Response(132, 4, SlaveBusy)

count=1
10020 4 6 Exception Response(132, 4, SlaveBusy)
10032 4 6 Exception Response(132, 4, SlaveBusy)
10052 4 6 Exception Response(132, 4, SlaveBusy)
10055 4 6 Exception Response(132, 4, SlaveBusy)
10058 4 6 Exception Response(132, 4, SlaveBusy)
10061 4 6 Exception Response(132, 4, SlaveBusy)
10064 4 6 Exception Response(132, 4, SlaveBusy)
10100 4 6 Exception Response(132, 4, SlaveBusy)
10140 4 6 Exception Response(132, 4, SlaveBusy)
10500 4 6 Exception Response(132, 4, SlaveBusy)
10504 4 6 Exception Response(132, 4, SlaveBusy)
10700 4 6 Exception Response(132, 4, SlaveBusy)
10800 4 6 Exception Response(132, 4, SlaveBusy)
11200 4 6 Exception Response(132, 4, SlaveBusy)
11300 4 6 Exception Response(132, 4, SlaveBusy)
11500 4 6 Exception Response(132, 4, SlaveBusy)
11800 4 6 Exception Response(132, 4, SlaveBusy)

count=4
"""
