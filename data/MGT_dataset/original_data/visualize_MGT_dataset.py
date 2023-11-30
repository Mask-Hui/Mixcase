import json
import matplotlib.pyplot as plt
import numpy as np
import csv

# 读取JSON文件
with open('MGT_original_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 统计每个对象的MGT_sentence词数
word_counts = [len(item['MGT_sentence'].split()) for item in data]

# 设置每个bin的范围和数量
bin_width = 9
min_val = min(word_counts)
max_val = max(word_counts)
num_bins = int((max_val - min_val) / bin_width) + 1

# 获取直方图数据
hist, bin_edges = np.histogram(word_counts, bins=num_bins, range=(min_val, max_val))

# 输出每个范围和具体数值到CSV文件
with open('word_count_frequency.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['词数范围', '个数'])
    for i in range(len(hist)):
        csv_writer.writerow([f"{int(bin_edges[i])} - {int(bin_edges[i+1])}", hist[i]])

# 绘制直方图（可选）
plt.hist(word_counts, bins=num_bins, color='skyblue', edgecolor='black')
plt.xlabel('Word Count')
plt.ylabel('Frequency')
plt.title('Word Count Distribution of MGT_sentence (Bin Width: 9 words)')
plt.grid(True)
plt.show()
