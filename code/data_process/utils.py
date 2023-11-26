import json


def get_categories(filename='../config/config.json'):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config['data_preprocessing']['categories']
