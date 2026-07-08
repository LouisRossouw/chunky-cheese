import json


def read_json(json_path):
    """ Reads json file """

    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)
