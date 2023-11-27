import os
import random
import json
import nltk
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize,word_tokenize
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


def filter_text(text, target_mean=150, target_variance=50):
    sentences = sent_tokenize(text)
    words_per_sentence = [len(word_tokenize(sentence)) for sentence in sentences]

    # 正态分布取样目标单词总数
    target_total_words = int(random.normalvariate(target_mean, target_variance))

    accepted_sentences = []
    total_words = 0
    for sentence, word_count in zip(sentences, words_per_sentence):
        if total_words + word_count > target_total_words:
            break
        accepted_sentences.append(sentence)
        total_words += word_count

    sampled_text = ' '.join(accepted_sentences)
    return sampled_text if total_words >= target_mean else None


def process_text_files(input_path, output_path):
    all_files = [f for f in os.listdir(input_path) if f.endswith('.txt')]
    random.shuffle(all_files)

    json_data = []
    entry_id = 1

    for file_name in all_files:
        if len(json_data) >= 50:
            break

        file_path = os.path.join(input_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            filtered_text = filter_text(text)

            if filtered_text:
                data_entry = {
                    #  category要写成6个
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

    # Reading JSON file and plotting text length distribution
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
    # 缺少MGT的处理
    process_text_files("../../data/HWT_dataset/original_long_data",
                       "../../data/HWT_dataset/original_data/HWT_original_data.json")