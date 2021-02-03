import ZipManager, SendProgram, PlayProgram, ChangeTextContent, DevicesManager
import time
import json
import serial.rs485

ser = None


def editJsonForWeatherData(text):
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


def initRS485():
    global ser
    ser = serial.serialposix.Serial(port="/dev/ttyCOM2",
                                    baudrate=19200,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE)
    ser.rs485_mode = serial.rs485.RS485Settings()
    return ser


def getWeatherData():
    global ser
    if ser is None:
        ser = initRS485()
    if ser.isOpen():
        print("it is open now")
        # ser.reset_input_buffer
        ser.write("0R0\r\n".encode(encoding='ascii'))
        weather_data = ser.readline()
        print(weather_data)
        return weather_data
    else:
        return "None"

if __name__ == '__main__':
    editJsonForWeatherData(str(getWeatherData()))
    ZipManager.getZip()
    SendProgram.sendProgram("program")
    PlayProgram.playProgram("program")
