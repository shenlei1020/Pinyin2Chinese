#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import my_model
import my_method
import json

###################################################################

curt_path = os.getcwd()
curt_dir = os.listdir()
relat_dict = my_model.hmm_mat.load_py_ch_relat()

# train_str = my_model.hmm_mat.read_material()
# range_str = my_model.hmm_mat.load_ch_range()

"""导入初始状态序列"""
if ('init_dict_p.txt' in curt_dir) and ('init_dict.txt' in curt_dir) and ('init_key_str.txt' in curt_dir):
    f = open('init_dict_p.txt', 'r', encoding='utf-8')
    init_dict_p = eval(f.read())
    f.close()

    h = open('init_dict.txt', 'r', encoding='utf-8')
    init_dict = eval(h.read())
    h.close()

    g = open('init_key_str.txt', 'r', encoding='utf-8')
    init_key_str = g.read()
    g.close()

else:
    print('Please run train_trans_mat_dict.py first!')
    exit()

"""导入概率转移矩阵"""
f_trans = open('trans_mat_dict.json', 'r')
trans_mat_dict = json.load(f_trans)
f_trans.close()

###################################################################
"""测试脚本"""
###################
"""输入文件拼音"""
arg_list = sys.argv
# arg_list = ['pinyin.py', 'input.txt', 'output.txt']
if not (arg_list[1] in curt_dir):
    raise ValueError('no such input file')
f_input = open(arg_list[1], 'r', encoding='utf-8')
py_temp = f_input.readlines()
f_input.close()
py_tot_list_r = [x.strip() for x in py_temp]
py_tot_list = [x.lower() for x in py_tot_list_r]
ch_tot_str = ''

for x in py_tot_list:
    pinyin_list = x.split()
    output_ch_str = my_method.viterbi.viterbi(pinyin_list, relat_dict, init_dict_p, trans_mat_dict)
    ch_tot_str = ch_tot_str + output_ch_str

"""输出识别汉字文件"""
f_output = open(arg_list[2], 'w', encoding='gbk')
f_output.write(ch_tot_str)
f_output.close()

"""计算准确率"""
test_file = 'test_' + arg_list[2]
f_otp_test = open(test_file, 'r', encoding='gbk')
test_output_str = f_otp_test.read()
test_output_str = test_output_str.replace(' ', '')
f_otp_test.close()

test_output_list = list(test_output_str)
ch_tot_list = list(ch_tot_str)

if not (len(test_output_list) == len(ch_tot_list)):
    print('the test file is wrong!')
    print('generate file length is', len(ch_tot_list))
    print('test file length is', len(test_output_list))
    exit()

cor_num = 0

for i in range(len(ch_tot_list)):
    if ch_tot_list[i] == test_output_list[i]:
        cor_num = cor_num + 1

cor_rate = cor_num/len(test_output_list)

print('总共%s个字，正确%s个字' % (str(len(test_output_list)), str(cor_num)))
print('正确率有：%s' % (str(cor_rate)))
