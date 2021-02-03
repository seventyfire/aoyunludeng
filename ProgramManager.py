import socket
import json
import os

READ = True
UNREAD = False
device_ip = '192.168.0.77'
device_port = 3333
config_status = UNREAD


def readConfig():
    global config_status
    if config_status == UNREAD:
        updateConfig()
        config_status = READ


def updateConfig():
    try:
        file = open('Device_Info', 'r')
        text = file.read()
        file.close()
        configs = text.split('\n')
        global device_port, device_ip
        device_ip = configs[0][3:]
        device_port = configs[1][5:]
    except Exception as e:
        print(e)
    finally:
        file.close()


def getDataStreamFromJsonFormattedStr(string):
    return str.encode(string, encoding='ascii')


def playProgram(program_name):
    readConfig()
    try:
        sk = socket.socket()
        sk.connect((device_ip, int(device_port)))
        program_name += ".zip"
        play_signal = json.dumps(
            {"_type": "playZipTask", "proName": program_name, "zVer": "xixun1"})
        print(play_signal)
        sk.send(getDataStreamFromJsonFormattedStr(play_signal))
    except Exception as e:
        print(e)
    finally:
        sk.close()


def getDataStreamFromJsonFormattedStr(string):
    return str.encode(string, encoding='ascii')


def checkZipOutputDir():
    if os.path.exists("ZipOutput") is False:
        os.mkdir("ZipOutput")


def sendProgram(program_name):
    readConfig()
    try:
        sk = socket.socket()
        sk.connect((device_ip, device_port))

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


if __name__ == '__main__':
    playProgram('program')
