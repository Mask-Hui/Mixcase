import os
import random
import json
import nltk
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize
import numpy as np


def read_text_files(input_path, num_samples=50):
    txt_files = [file for file in os.listdir(input_path) if file.endswith('.txt')]
    if len(txt_files) < num_samples:
        num_samples = len(txt_files)
    chosen_files = random.sample(txt_files, num_samples)
    return chosen_files


def calculate_words_per_sentence(text):
    sentences = sent_tokenize(text)
    words_count = [len(nltk.word_tokenize(sentence)) for sentence in sentences]
    return words_count


def filter_text(text, target_mean=100, target_variance=20):
    sentences = sent_tokenize(text)
    words_per_sentence = [len(nltk.word_tokenize(sentence)) for sentence in sentences]

    accepted_sentences = []
    total_words = 0
    for i, word_count in enumerate(words_per_sentence):
        accepted_sentences.append(sentences[i])
        total_words += word_count

        # 检查是否达到目标平均单词数
        if total_words >= target_mean:
            break

    sampled_text = ' '.join(accepted_sentences)
    return sampled_text if total_words >= target_mean else None


def process_text_files(input_path, output_path):
    clean_text_files(input_path)
    chosen_files = read_text_files(input_path)
    json_data = []
    entry_id = 1

    for file_name in chosen_files:
        file_path = os.path.join(input_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            words_per_sentence = calculate_words_per_sentence(text)
            # 好像是每个文件按正态分布取的
            avg_words_per_sentence = sum(words_per_sentence) / len(words_per_sentence)
            # 缺少方差
            filtered_text = filter_text(text, target_mean=avg_words_per_sentence)

            if filtered_text:
                data_entry = {
                    "category": "",
                    "id": entry_id,
                    "HWT_sentence": filtered_text
                }
                json_data.append(data_entry)
                entry_id += 1

    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(json_data, output_file, indent=4)

    # 画图
    # Reading JSON file and plotting text length distribution
    file_path = "../../data/HWT_dataset/original_data/HWT_original_data.json"
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    text_lengths = [len(item['HWT_sentence'].split()) for item in data]

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