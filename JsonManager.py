import json


def readJson():
    with open("./ZipInput/program") as file_obj:
        return json.load(file_obj)

def saveJson(json_dict):
    with open("./ZipInput/program", 'w') as file:
        json.dump(json_dict, file, indent=4)