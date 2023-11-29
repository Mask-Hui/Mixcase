import os
import random
import json
import matplotlib.pyplot as plt
import scipy.stats as stats
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
from utils import *


def calculate_interval_counts(total_count):
    target_mean = 80
    target_variance = 20
    intervals = [(i, i + 20) for i in range(target_mean - 2 * target_variance, target_mean + 2 * target_variance, 20)]
    probabilities = [
        stats.norm(target_mean, target_variance).cdf(interval[1]) - stats.norm(target_mean, target_variance).cdf(
            interval[0]) for interval in intervals]
    total_prob = sum(probabilities)
    interval_counts = {interval: int(prob / total_prob * total_count) for interval, prob in
                       zip(intervals, probabilities)}
    for interval, count in interval_counts.items():
        print(f"Interval {interval}: {count} texts")
    return interval_counts


def filter_text(text, target_interval):
    sentences = sent_tokenize(text)
    words_per_sentence = [len(word_tokenize(sentence)) for sentence in sentences]
    accepted_sentences = []
    total_words = 0
    index = 0

    while sentences and index < len(sentences) and total_words < target_interval[1]:
        next_sentence = sentences[index]
        next_word_count = words_per_sentence[index]
        if target_interval[0] <= next_word_count <= target_interval[1]:
            accepted_sentences.append(next_sentence)
            total_words += next_word_count
        index += 1
        sentences.pop(0)
        words_per_sentence.pop(0)

    return ' '.join(accepted_sentences) if accepted_sentences else None


def process_HWT_text_files(input_path, output_path):
    max_sampling_tries = 3
    desired_samples_per_category = 52
    categories = get_categories()
    json_data = []
    entry_id = 1

    for category in categories:
        interval_counts = calculate_interval_counts(desired_samples_per_category)
        sorted_intervals = sorted(interval_counts.items(), key=lambda x: x[0])

        category_path = os.path.join(input_path, category)
        clean_text_files(category_path)
        all_txt_files = [file for file in os.listdir(category_path) if file.endswith('.txt')]
        processed_files = set()
        valid_samples_count = 0

        while valid_samples_count < desired_samples_per_category and all_txt_files:
            remaining_files = list(set(all_txt_files) - processed_files)
            if not remaining_files:
                break

            random.shuffle(remaining_files)

            for interval, count in sorted_intervals:
                if count > 0:
                    for file_name in remaining_files:
                        if valid_samples_count >= desired_samples_per_category:
                            break

                        if file_name in processed_files:
                            continue

                        file_path = os.path.join(category_path, file_name)
                        sampling_tries = 0

                        while sampling_tries < max_sampling_tries:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                text = file.read()
                                filtered_text = filter_text(text, interval)
                                if filtered_text:
                                    interval_counts[interval] -= 1
                                    valid_samples_count += 1
                                    data_entry = {
                                        "category": category,
                                        "id": entry_id,
                                        "HWT_sentence": filtered_text
                                    }
                                    json_data.append(data_entry)
                                    entry_id += 1
                                    processed_files.add(file_name)
                                    break
                            sampling_tries += 1

                        if sampling_tries >= max_sampling_tries:
                            processed_files.add(file_name)

        print(
            f"Category: {category}, Total Files: {len(all_txt_files)}, Chosen Files: {len(processed_files)}, Valid Samples: {valid_samples_count}")

    save_and_plot(json_data, output_path, 'HWT_sentence')


def process_MGT_text_files(input_path, output_path):
    max_sampling_tries = 3
    desired_samples_per_category = 105
    categories = get_datasets()
    json_data = []
    entry_id = 1

    for category in categories:
        interval_counts = calculate_interval_counts(desired_samples_per_category)
        sorted_intervals = sorted(interval_counts.items(), key=lambda x: x[0])

        category_path = os.path.join(input_path, category)
        clean_text_files(category_path)
        all_txt_files = [file for file in os.listdir(category_path) if file.endswith('.txt')]
        processed_files = set()
        valid_samples_count = 0

        while valid_samples_count < desired_samples_per_category and all_txt_files:
            remaining_files = list(set(all_txt_files) - processed_files)
            if not remaining_files:
                break

            random.shuffle(remaining_files)

            for interval, count in sorted_intervals:
                if count > 0:
                    for file_name in remaining_files:
                        if valid_samples_count >= desired_samples_per_category:
                            break

                        if file_name in processed_files:
                            continue

                        file_path = os.path.join(category_path, file_name)
                        sampling_tries = 0

                        while sampling_tries < max_sampling_tries:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                text = file.read()
                                filtered_text = filter_text(text, interval)
                                if filtered_text:
                                    valid_samples_count += 1
                                    model_label = file_name.split('_')[2]
                                    data_entry = {
                                        "category": category,
                                        "model": model_label,
                                        "id": entry_id,
                                        "MGT_sentence": filtered_text
                                    }
                                    json_data.append(data_entry)
                                    entry_id += 1
                                    processed_files.add(file_name)
                                    break
                            sampling_tries += 1

                        if sampling_tries >= max_sampling_tries:
                            processed_files.add(file_name)
        print(f"Category: {category}, Total Files: {len(all_txt_files)}, Chosen Files: {len(processed_files)}, Valid Samples: {valid_samples_count}")
    save_and_plot(json_data, output_path, 'MGT_sentence')


def save_and_plot(json_data, output_path, key):
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(json_data, output_file, indent=4)

    text_lengths = [len(item[key].split()) for item in json_data]
    max_length = max(text_lengths)
    bins = list(range(0, max_length + 10, 10))
    bins.append(max_length + 5)
    bins.sort()

    counts, bins, patches = plt.hist(text_lengths, bins=bins, alpha=0.7, color='blue')

    for count, patch in zip(counts, patches):
        plt.text(patch.get_x() + patch.get_width() / 2, patch.get_height(),
                 f'{int(count)}', ha='center', va='bottom')

    plt.xlabel('Text Length (in words)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Text Lengths')
    plt.show()


def clean_text_files(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    content = input_file.read()

                cleaned_content = ' '.join(content.split())

                sentences = cleaned_content.split('. ')
                cleaned_sentences = [sentence.capitalize() for sentence in sentences]
                cleaned_content = '. '.join(cleaned_sentences)

                with open(file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(cleaned_content)


if __name__ == "__main__":
    # process_HWT_text_files("../../data/HWT_dataset/original_long_data",
                           # "../../data/HWT_dataset/original_data/HWT_original_data.json")
    process_MGT_text_files("../../data/MGT_dataset/original_long_data",
                           "../../data/MGT_dataset/original_data/MGT_original_data.json")
