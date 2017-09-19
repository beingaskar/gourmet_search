import json


def load_json_data(file_path):
    """
    Returns the json data from given json file path.
    """

    try:
        with open(file_path) as f:
            data = json.load(f)
    except:
        return None

    return data
