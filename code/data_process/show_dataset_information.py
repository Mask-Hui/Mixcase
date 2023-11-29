import os
from collections import Counter

def get_word_count(text):
    words = text.split()
    return len(words)

def analyze_folder(folder_path):
    subfolders = [subfolder for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]

    for subfolder in subfolders:
        print(f"Analysis for folder: {subfolder}")
        subfolder_path = os.path.join(folder_path, subfolder)
        txt_files = [os.path.join(subfolder_path, file) for file in os.listdir(subfolder_path) if file.endswith('.txt')]

        all_word_counts = []
        for txt_file in txt_files:
            with open(txt_file, 'r', encoding='utf-8') as file:
                content = file.read()
                sentences = content.split('.')  # Assuming sentences are separated by '.'

                word_counts = [get_word_count(sentence) for sentence in sentences]
                all_word_counts.extend(word_counts)

        if all_word_counts:
            average_word_count = sum(all_word_counts) / len(all_word_counts)
            max_word_count = max(all_word_counts)
            print(f"Average word count per sentence in folder {subfolder}: {average_word_count}")
            print(f"Max word count in a sentence in folder {subfolder}: {max_word_count}\n")
        else:
            print(f"No text files found in folder {subfolder}\n")

# 输入文件夹路径
folder_path = "../../data/MGT_dataset/original_long_data"
analyze_folder(folder_path)
