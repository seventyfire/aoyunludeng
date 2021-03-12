class Program:
    def __init__(self, json_data=None, program_name="program", zip_file_path=None, zip_file_size=None):
        self.json_data = json_data  # receive front-end's json data
        self.zip_file_path = zip_file_path  # store program zip file's path
        self.zip_file_size = zip_file_size  # store program zip file's size
        self.program_name = program_name

    # this function will clear all of the content in the program file
    def write_json_data(self):
        import json
        import os
        if os.path.exists("ZipOutput") is False:
            os.mkdir("ZipOutput")
        program_file = open("./ZipInput/" + "program", "w")
        # json.dump(self.json_data, program_file)
        program_file.write(self.json_data)
        program_file.flush()
        program_file.close()

    def get_json_data(self):
        return self.json_data

    def set_json_data(self, json_data):
        self.json_data = json_data

    # return relative path of the zip file
    def get_zip_file(self):
        print("zip")
        import os
        import zipfile
        import time
        if os.path.exists("ZipOutput") is False:
            os.mkdir("ZipOutput")
        self.program_name = str(time.time()).replace(".", "")
        zip_path = "./ZipOutput/" + self.program_name + ".zip"
        print("program name is: " + self.program_name)
        z = zipfile.ZipFile(zip_path, 'w')

        if os.path.isdir("ZipInput"):
            for file in os.listdir("ZipInput"):
                print(file)
                z.write("ZipInput" + os.sep + file, file)
        else:
            print("can not find ZipInput")
        z.close()
        return zip_path

    def clear_resources(self):
        import os, shutil
        folder = './ZipOutput'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        folder = './ZipInput'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def send_program(self):
        from connector import Connector
        import socket
        import os
        import json

        connector = Connector()
        
        self.write_json_data()
        zip_file_relative_path = self.get_zip_file()
        sk = socket.socket()
        try:
            sk.connect((connector.ip, int(connector.port)))

            file_size = os.stat(zip_file_relative_path)

            start_signal = json.dumps(
                {"_type": "fileStart", "id": self.program_name + ".zip", "relative_path": "", "size": file_size.st_size,
                 "zVer": "xixun1"})
            print(start_signal)
            sk.send(str.encode(start_signal, encoding='ascii'))

            file = open(zip_file_relative_path, "rb")
            file_data = file.read()
            sk.send(file_data)
            file.close()

            end_signal = json.dumps({"_type": "fileEnd", "id": self.program_name + ".zip", "zVer": "xixun1"})
            print(end_signal)
            sk.send(str.encode(end_signal, encoding='ascii'))
        except Exception as e:
            print(e)
        finally:
            sk.close()
        print("after send, program name is :" + self.program_name)
        return str(self.program_name)

    def play_program(self, program_name):
        from connector import Connector
        import socket
        import json
        sk = socket.socket()
        print("play")
        try:
            connector = Connector()
            sk.connect((connector.ip, int(connector.port)))
            play_signal = json.dumps(
                    {"_type": "playZipTask", "proName": str(program_name) + ".zip", "zVer": "xixun1"})
            print(play_signal)
            sk.send(str.encode(play_signal, encoding='ascii'))
        except Exception as e:
            print(e)
        finally:
            sk.close()

