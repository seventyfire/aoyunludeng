import json
import requests
import base64

message = "80"
bytes_message = message.encode("utf-8")
bytes_message = base64.b64encode(bytes_message)
str_message = str(bytes_message)[2:-1]
print(str_message)
command = {"_id": "98e8d3cd47fad6ce8e3f7b8d42cb4d9a",
           "_type": "SetRealtimeMessage",
           "message": str_message,
           "width": 30,
           "left": 40,
           "windowBackground": 0,
           "verticalPos": 1,
           "horizontalPos": 0,
           "fontBackground": 0,
           "fontColor": 0xFFFFFFFF,
           "fontSize": 12,
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
