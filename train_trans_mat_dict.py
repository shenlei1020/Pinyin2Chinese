#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import my_model
import json

###################################################################
"""导入所需参数"""
curt_path = os.getcwd()
curt_dir = os.listdir()

relat_dict = my_model.hmm_mat.load_py_ch_relat()
train_str = my_model.hmm_mat.read_material()
range_str = my_model.hmm_mat.load_ch_range()

"""导入初始状态概率"""
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
    init_mat = my_model.hmm_mat.Initmat(train_str, range_str)
    init_dict, init_dict_p, init_key_str = init_mat.genermat()
    f = open('init_dict_p.txt', 'w', encoding='utf-8')
    f.write(str(init_dict_p))
    f.close()
    h = open('init_dict.txt', 'w', encoding='utf-8')
    h.write(str(init_dict))
    h.close()
    g = open('init_key_str.txt', 'w', encoding='utf-8')
    g.write(init_key_str)
    g.close()

"""生成概率转移矩阵"""
if 'trans_mat_dict.json' in curt_dir:
    print('trans_mat_dict.json already exist!')
    exit()
trans_mat = my_model.hmm_mat.Transmat(train_str, init_dict, init_dict_p)
trans_mat_dict = trans_mat.genermat(init_key_str)

f_trans = open('trans_mat_dict.json', 'w')
json.dump(trans_mat_dict, f_trans)
f_trans.close()

print('trans_mat_dict.txt is done!')
###################################################################