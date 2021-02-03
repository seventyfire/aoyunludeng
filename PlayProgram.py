import socket
import json


def getDataStreamFromJsonFormattedStr(string):
    return str.encode(string, encoding='ascii')

def playProgram(program_name):
    sk = socket.socket()
    sk.connect(('192.168.0.77', 3333))
    program_name += ".zip"
    try:
        play_signal = json.dumps(
            {"_type":"playZipTask","proName":program_name,"zVer":"xixun1"})
        print(play_signal)
        sk.send(getDataStreamFromJsonFormattedStr(play_signal))
    except:
        print("error")
    finally:
        sk.close()
if __name__ == "__main__":
    playProgram()
