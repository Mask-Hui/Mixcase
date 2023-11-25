import os
import nltk
from utils import *


# clean text
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


# split original txt files by sentence
def split_txt_by_sentences(input_folder, output_folder):
    domains = get_categories()

    for domain in domains:
        domain_folder = os.path.join(input_folder, domain)
        if not os.path.exists(domain_folder):
            continue

        output_domain_folder = os.path.join(output_folder, domain)
        os.makedirs(output_domain_folder, exist_ok=True)

        for root, _, files in os.walk(domain_folder):
            for file in files:
                if file.endswith('.txt'):
                    input_file_path = os.path.join(root, file)
                    output_file_path = os.path.join(output_domain_folder, file)

                    with open(input_file_path, 'r', encoding='utf-8') as input_file:
                        content = input_file.read()

                    sentences = nltk.sent_tokenize(content)
                    result = []

                    i = 0
                    while i < len(sentences):
                        current_sentence = sentences[i].strip()
                        # 检查句子是否少于或等于2个词
                        if len(current_sentence.split()) <= 2 and i + 1 < len(sentences):
                            # 将当前句子与下一个句子合并
                            result.append((current_sentence + ' ' + sentences[i + 1]).strip())
                            i += 2
                        else:
                            result.append(current_sentence)
                            i += 1

                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        for sentence in result:
                            output_file.write(sentence + '\n')


# merge single txt files
def merge_txt_files(input_folder, output_folder):
    domains = get_categories()

    for domain in domains:
        domain_folder = os.path.join(input_folder, domain)
        if not os.path.exists(domain_folder):
            continue

        output_domain_folder = os.path.join(output_folder, domain)
        os.makedirs(output_domain_folder, exist_ok=True)

        output_file_path = os.path.join(output_domain_folder, f"{domain}_merged.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for root, _, files in os.walk(domain_folder):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as input_file:
                            content = input_file.read()
                            output_file.write(content)

        clean_text_files(output_folder)
        split_txt_by_sentences(output_folder, output_folder)


def process_text_to_json(input_folder, output_folder):
    domains = get_categories()
    data_list = []

    for domain in domains:
        domain_folder = os.path.join(input_folder, domain)
        if not os.path.exists(domain_folder):
            continue

        for root, _, files in os.walk(domain_folder):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)

                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        lines = input_file.readlines()
                        for index, line in enumerate(lines, start=1):
                            data = {
                                "category": domain,
                                "id": index,
                                "original_sentence": line.strip()  # 移除行尾换行符
                            }
                            data_list.append(data)

    os.makedirs(output_folder, exist_ok=True)
    output_json = os.path.join(output_folder, 'original_sentence.json')

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    merge_txt_files('../../data/original_long_data', '../../data/original_data')
    process_text_to_json('../../data/original_data', '../../data/original_data')
