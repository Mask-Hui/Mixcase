△config
	· config.h:存储配置信息，如API、categories的名称等

△data_process（数据处理的文件夹）
	· utils.py:包含了一些通用的、可重复利用的功能函数，如get_categories()
	· data_preprocessing.py:将数据集的.txt文件，按照正态分布挑选出block并存入json文件

△data;
    HWT_dataset:
        · original_long_data:原始长句子的n多txt
        · original_data: 整合成的原始数据集original_sentence.json
    MGT_dataset: