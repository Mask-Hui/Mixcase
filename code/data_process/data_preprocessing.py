import os
import random
import json
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize,word_tokenize
import numpy as np
from utils import *


def filter_text(text, target_mean=150, target_variance=20, tolerance_percentage=0.30):
    sentences = sent_tokenize(text)
    words_per_sentence = [len(word_tokenize(sentence)) for sentence in sentences]

    target_total_words = int(random.normalvariate(target_mean, target_variance))

    accepted_sentences = []
    total_words = 0
    for sentence, word_count in zip(sentences, words_per_sentence):
        if total_words + word_count > target_total_words:
            break
        accepted_sentences.append(sentence)
        total_words += word_count

    lower_bound = target_mean - (target_mean * tolerance_percentage)
    upper_bound = target_mean + (target_mean * tolerance_percentage)

    # 检查总单词数是否在容忍区间内
    if lower_bound <= total_words <= upper_bound:
        return ' '.join(accepted_sentences)
    else:
        return None


def process_text_files(input_path, output_path):
    desired_samples_per_category = 50
    categories = get_categories()
    json_data = []
    entry_id = 1

    for category in categories:
        category_path = os.path.join(input_path, category)
        clean_text_files(category_path)
        txt_files = [file for file in os.listdir(category_path) if file.endswith('.txt')]
        random.shuffle(txt_files)  # 随机打乱文件列表

        chosen_files = set()
        valid_samples_count = 0  # 记录符合要求的样本数量
        for file_name in txt_files:
            if valid_samples_count >= desired_samples_per_category:
                break  # 如果已经达到所需有效样本数，则停止

            if file_name not in chosen_files:
                chosen_files.add(file_name)
                file_path = os.path.join(category_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    filtered_text = filter_text(text)

                    if filtered_text:
                        valid_samples_count += 1
                        data_entry = {
                            "category": category,
                            "id": entry_id,
                            "HWT_sentence": filtered_text
                        }
                        json_data.append(data_entry)
                        entry_id += 1

        print(f"Category: {category}, Total Files: {len(txt_files)}, Chosen Files: {len(chosen_files)}, Valid Samples: {valid_samples_count}")

    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(json_data, output_file, indent=4)

    text_lengths = [len(item['HWT_sentence'].split()) for item in json_data]

    plt.hist(text_lengths, bins=20, alpha=0.7, color='blue')
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
    process_text_files("../../data/HWT_dataset/original_long_data",
                       "../../data/HWT_dataset/original_data/HWT_original_data.json")
