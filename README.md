# Mixcase

## config
	· config.h:存储配置信息，如API、categories的名称等

## data_process（数据处理的文件夹）
	· utils.py:包含了一些通用的、可重复利用的功能函数，如get_categories()
	· txt_to_json.py:把每个category的很多个txt文件合并成一个大的txt→对txt文件进行clean（开头字母大写、正则切分）→改写为json文件
	· compose_split_sentence.py:将原始json文件中的句子进行组合，长度在100-280 letters
	· select_split_sentence.py:访问data\split_data\compose_data.json中blocks的数量，然后在原始split的json文件中找到句子长度最短的相同数量的数据，并写入data\split_data\select_data.json

## data
	· original_long_data:原始长句子的n多txt
	· original_data:txt按category合为一个大的txt文件  and  整合成的原始数据集original_sentence.json
	· split_data:包含select和compose两种（即数据集1和2）
