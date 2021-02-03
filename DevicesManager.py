import serial.rs485

ser = None


def initRS485():
    global ser
    ser = serial.serialposix.Serial(port="/dev/ttyCOM2",
                                    baudrate=19200,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE)
    ser.rs485_mode = serial.rs485.RS485Settings()


def getWeatherData():
    if ser is None:
        initRS485()
    if ser.isOpen():
        print("it is open now")
        ser.reset_input_buffer
        ser.write("0R0\r\n".encode(encoding='ascii'))
        temp = ser.readline()
        print(temp)
        return temp
    else:
        return "None"
