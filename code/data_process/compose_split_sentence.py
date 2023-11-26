import os
from utils import *


def read_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_json_data(file_path, data):
    category_id_counter = {}
    categorized_data = {}

    for block in data:
        category = block['category']
        if category not in categorized_data:
            categorized_data[category] = []
            category_id_counter[category] = 1

        categorized_data[category].append(block)

    for category, category_blocks in categorized_data.items():
        for block in category_blocks:
            block['id'] = category_id_counter[category]
            category_id_counter[category] += 1

    combined_data = [block for category_blocks in categorized_data.values() for block in category_blocks]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(combined_data, file, indent=4)


def process_data(original_data):
    categories = get_categories()
    block_data = []

    for category in categories:
        category_data = [entry for entry in original_data if entry['category'] == category]
        current_block = {
            "category": category,
            "id": 1,
            "type": "block",
            "HWT_sentence": ""
        }

        for entry in category_data:
            original_sentence = entry['original_sentence']
            sentence_length = len(original_sentence)

            if sentence_length > 280:
                block_data.append({
                    "category": category,
                    "id": current_block['id'],
                    "type": "block",
                    "HWT_sentence": original_sentence
                })
                current_block['id'] += 1
            else:
                if 100 <= len(current_block['HWT_sentence']) + sentence_length <= 280:
                    current_block['HWT_sentence'] += original_sentence + ' '
                else:
                    block_data.append(current_block)
                    current_block = {
                        "category": category,
                        "id": current_block['id'] + 1,
                        "type": "block",
                        "HWT_sentence": original_sentence + ' '
                    }

        if current_block['HWT_sentence']:
            block_data.append(current_block)

    return block_data


def run_compose_process(input_path, output_path):
    if os.path.exists(input_path):
        original_data = read_json_data(input_path)
        processed_data = process_data(original_data)
        if processed_data:
            write_json_data(output_path, processed_data)
        else:
            print("No data_HWT meeting the criteria.")
    else:
        print("Original data_HWT file not found.")


if __name__ == "__main__":
    run_compose_process('../../data_HWT/original_data/original_sentence.json',
                        '../../data_HWT/split_data/compose_data.json')
