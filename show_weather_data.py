import ZipManager, SendProgram, PlayProgram, ChangeTextContent, DevicesManager
import time
import json


def changeText(text):
    data_array = text.split(',')
    text = data_array[6]
    json = readJson()
    json["task"]["items"][0]["_program"]["layers"][0]["sources"][0]["html"] = \
        "<p style='font-size:12px'>" + text + "</p>"
    saveJson(json)


def readJson():
    with open("./ZipInput/program") as file_obj:
        return json.load(file_obj)


def saveJson(json_dict):
    with open("./ZipInput/program", 'w') as file:
        json.dump(json_dict, file)


if __name__ == '__main__':
    changeText(str(DevicesManager.getData()))
    ZipManager.getZip()
    SendProgram.sendProgram("program")
    PlayProgram.playProgram("program")
