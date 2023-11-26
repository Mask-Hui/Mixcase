import os
from utils import *


def read_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_json_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def get_category_counts(compose_data):
    category_counts = {}
    for entry in compose_data:
        category = entry['category']
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1
    return category_counts


def get_shortest_sentences(original_data, category_counts):
    select_data = []
    for category, count in category_counts.items():
        category_data = [entry for entry in original_data if entry['category'] == category]
        category_data.sort(key=lambda x: len(x['original_sentence']))
        for i in range(count):
            select_entry = {
                "category": category,
                "id": i + 1,
                "type": "short",
                "HWT_sentence": category_data[i]['original_sentence']
            }
            select_data.append(select_entry)
    return select_data


def run_select_process(block_path, source_path, output_path):
    original_data = read_json_data(source_path)
    compose_data = read_json_data(block_path)

    category_counts = get_category_counts(compose_data)
    select_data = get_shortest_sentences(original_data, category_counts)

    output_folder = os.path.dirname(output_path)
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output directory exists

    write_json_data(output_path, select_data)


if __name__ == "__main__":
    run_select_process('../../data_HWT/split_data/compose_data.json',
                       '../../data_HWT/original_data/original_sentence.json',
                       '../../data_HWT/split_data/select_data.json')
