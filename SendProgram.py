import requests
import json

# data = {
#     "type": "commandXixunPlayer",
#     "command": {
#         "_type": "PlayXixunTask",
#
#         "task": {
#             "_id": "55f5b637-a529-4807-8063-deeb3c12f9ab",
#             "name": "demo",
#             "_department": None,
#
#             "items": [
#                 {
#                     "_id": "0d10f114-b93d-4eb7-a1a7-60311eeab6b2",
#
#                     "_program": {
#                         "_id": "5c909eca4477c9247940613b",
#
#                         "totalSize": 14545722,
#                         "name": "name",
#                         "width": 300,
#                         "height": 240,
#                         "_company": "alahover",
#                         "_department": "539eaaedb6e1232a1566d9c2",
#                         "_role": "539eaaedb6e1232a1566d9c3",
#                         "_user": "yzd",
#                         "__v": 0,
#                         "layers": [
#                             {
#                                 "repeat": False,
#                                 "sources": [
#                                     {
#                                         "id": "",
#                                         "name": "Countdown",
#                                         "_type": "Countdown",
#                                         "lineHeight": 1.4,
#                                         "time": "2014-5-1 10:30",
#                                         "html": "Remain<br />%dDay%hHours%mMins%sSecs",
#                                         "playTime": 37,
#                                         "timeSpan": 10,
#                                         "left": 0,
#                                         "top": 0,
#                                         "width": 150,
#                                         "height": 120,
#                                         "entryEffect": "None",
#                                         "exitEffect": "None",
#                                         "entryEffectTimeSpan": 0,
#                                         "exitEffectTimeSpan": 0
#                                     }
#                                 ]
#                             }
#                         ],
#                         "dateCreated": "2021-01-12T07:48:26.984Z"
#                     },
#                     "priority": 0,
#                     "repeatTimes": 1,
#                     "version": 0,
#                     "schedules": [
#                         {
#                             "dateType": "All",
#                             "startDate": None,
#                             "endDate": None,
#                             "timeType": "All",
#                             "startTime": None,
#                             "endTime": None,
#                             "filterType": "Week",
#                             "weekFilter": [
#                                 1,
#                                 2,
#                                 3
#                             ],
#                             "monthFilter": [
#                             ],
#                             "lng": "zh-CN"
#                         }
#                     ]
#                 }
#             ],
#             "executeDate": None,
#             "cmdId": "44f5b637-a529-4807-8063-deeb3c12f9ab"
#         }
#     }
# }
# # print(str(data))
import os
import socket


def getDataStreamFromJsonFormattedStr(string):
    return str.encode(string, encoding='ascii')


def checkZipOutputDir():
    if os.path.exists("ZipOutput") is False:
        os.mkdir("ZipOutput")


def sendProgram(program_name):
    try:
        sk = socket.socket()
        sk.connect(('192.168.0.77', 3333))

        file_name = program_name + ".zip"
        checkZipOutputDir()
        file_size = os.stat("./ZipOutput/" + file_name)

        start_signal = json.dumps(
            {"_type": "fileStart", "id": file_name, "relative_path": "", "size": file_size.st_size, "zVer": "xixun1"})
        print(start_signal)
        sk.send(getDataStreamFromJsonFormattedStr(start_signal))

        file = open("./ZipOutput/" + file_name, "rb")
        file_data = file.read()
        file.close()
        sk.send(file_data)

        end_signal = json.dumps({"_type": "fileEnd", "id": file_name, "zVer": "xixun1"})
        print(end_signal)
        sk.send(getDataStreamFromJsonFormattedStr(end_signal))
    except Exception as e:
        print(e)
    finally:
        sk.close()
