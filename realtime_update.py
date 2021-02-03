import base64
import json
import requests
import time

from pymodbus.client.sync import ModbusSerialClient

client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyCOM2',
    baudrate=19200,
    parity='N',
    stopbits=1,
    bytesize=8
)

while True:
    try:   # Trying for connect to Modbus Server/Slave
        '''Reading from a holding register with the below content.'''
        res = client.read_holding_registers(address=0, count=26, unit=48)

        if not res.isError():
            print(res.registers)
        else:
            print(res)

        message = str(res.registers[5])
        bytes_message = message.encode("utf-8")
        bytes_message = base64.b64encode(bytes_message)
        str_message = str(bytes_message)[2:-1]
        print(str_message)

        command = {"_id": "98e8d3cd47fad6ce8e3f7b8d42cb4d9b",
                    "_type": "SetRealtimeMessage",
                    "message": str_message,
                    "width": 64,
                    "left": 0,
                    "windowBackground": 0,
                    "verticalPos": 1,
                    "horizontalPos": 1,
                   "fontBackground": 0,
                   "fontColor": 0xFF00BFFF,
                   "fontSize": 24,
                   "lineSpace": 0,
                   "showType": 0,
                   "speed": 20,
                   "moveCount": 0,
                   "residenceTime": -1
                   }
        j = json.dumps(command)
        headers = {'Content-Type': 'text/plain'}
        r = requests.post("http://192.168.0.77:2016/settings", data=j, headers=headers)
        print(r.text)
        print("sleeping...")
        time.sleep(5)
    except Exception as e:
        print(e)
        client.close()
