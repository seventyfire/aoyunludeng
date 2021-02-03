import zipfile
import os
import sys


def getZip():
    if os.path.exists("ZipOutput") is False:
        os.mkdir("ZipOutput")
    zip_name = "./ZipOutput/program.zip"

    z = zipfile.ZipFile(zip_name, 'w')

    if os.path.isdir("ZipInput"):
        for file in os.listdir("ZipInput"):
            z.write("ZipInput" + os.sep + file, file)
        z.close()
    else:
        print("can not find ZipInput")


if __name__ == '__main__':
    print(sys.argv)
