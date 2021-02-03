import ZipManager, SendProgram, PlayProgram, JsonManager, SaveJson

def changeText(text):
    data_array = text.split(',')
    text = data_array[6]
    json = JsonManager.readJson()
    json["task"]["items"][0]["_program"]["layers"][0]["sources"][0]["html"] = \
            "<p style='font-size:12px'>" + text + "</p>"
    SaveJson.saveJson(json)



