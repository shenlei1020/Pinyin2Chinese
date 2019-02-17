1、常用汉字6763个，字母表中汉字7497（其中包含多音字）
2、train_trans_mat_dict.py脚本生成稀疏的初始状态矩阵和概率转移矩阵，由于提前已经生成两个矩阵，故不需再运行该脚本了。
3、init_dict.txt, init_dict_p.txt是初始状态矩阵文件，trans_mat_dict.json是概率转移矩阵文件。
3、拼音输入法调用格式：python pinyin.py input_1.txt output_1.txt。
其中input_1.txt是输入拼音文件，output_1.txt是脚本生成的识别汉字文件，test_output_1.txt是正确的汉字文件，用于正确性检验（脚本已集成计算正确率程序段，把正确的汉字文件命名为”test_[output_1.txt]”命名为即可）。
4、input_1.txt, input_2.txt和test_output_1.txt, test_output_2.txt是两对测试文件。