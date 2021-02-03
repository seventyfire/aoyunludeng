import json


def saveJson(json_dict):
    with open("./ZipInput/program", 'w') as file:
        json.dump(json_dict, file)


if __name__ == '__main__':
    j = {
        "_type": "PlayXixunTask",
        "task": {
            "items": [
                {
                    "_program": {
                        "layers": [
                            {
                                "sources": [
                                    {
                                        "_type": "SingleLineText",
                                        "html": "<p>Hello</p>",
                                        "width": 64,
                                        "height": 16,
                                        "timeSpan": 999999,
                                        "speed": 5
                                    },
                                    {
                                        "_type": "SingleLineText",
                                        "html": "<p>Go</p>",
                                        "width": 64,
                                        "height": 16,
                                        "timeSpan": 999999,
                                        "speed": 5,
                                        "top": 16
                                    }
                                ]
                            }
                        ]
                    },
                    "repeatTimes": 1
                }
            ]
        }
    }
    with open("test_it", 'w') as file:
        json.dump(j, file, indent=4)
