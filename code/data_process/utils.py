import json


def get_categories(filename='../config/config.json'):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config['data_preprocessing']['HWT_categories']


def get_datasets(filename='../config/config.json'):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config['data_preprocessing']['MGT_datasets:']