#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" generate the three matrix in hmm """

__author__ = 'Shen Lei'
__model_name__ = 'Hidden Markov Model'

import os
import re

def read_material():
    """this function is to read and clean raw data"""

    mod_path = os.path.dirname(os.path.abspath(__file__))
    curt_path = os.getcwd()
    os.chdir(mod_path)
    curt_dir = os.listdir()
    if 'train_str.txt' in curt_dir:
        f = open('train_str.txt', 'r', encoding='gbk')
        train_str = f.read()
        f.close()

        os.chdir(curt_path)
        return train_str

    dir_list = list(filter(lambda x: '2016' in x, curt_dir))

    data_str = ''
    for dir_name in dir_list:
        f = open(dir_name, 'r', encoding='gbk')
        temp_list = f.read()
        data_str = data_str + temp_list
        f.close()

    """clean data by remove ' ' and '\n'"""

    train_str = re.sub(r'[a-z]+|[A-Z]+|[0-9]+|\W+', 'S', data_str)
    train_str = re.sub(r'S+', 'S', train_str)

    """把语料库写成txt文件。默认不写"""
    f = open('train_str.txt', 'w', encoding='gbk')
    f.write(train_str)
    f.close()

    os.chdir(curt_path)
    return train_str

def load_py_ch_relat( wrt_down=0, relat_file='拼音汉字表.txt'):
    mod_path = os.path.dirname(os.path.abspath(__file__))
    curt_path = os.getcwd()
    os.chdir(mod_path)
    """判断有没有已生成的文件"""
    mod_dir = os.listdir()
    if 'py_ch_relat.txt' in mod_dir:
        f = open('py_ch_relat.txt', 'r', encoding='gbk')
        relat_pre = f.read()
        relat_dict = eval(relat_pre)
        f.close()

        os.chdir(curt_path)
        return relat_dict

    f_relat = open(relat_file, 'r', encoding='gbk')
    data_relat = f_relat.readlines()
    f_relat.close()

    temp1 = [x.strip() for x in data_relat]
    temp2 = [x.replace(' ', '') for x in temp1]
    relat_dict = {}
    for x in temp2:
        """利用正则表达式把拼音和汉字分离"""
        pinyin = ".*?([a-z]|([a-z].*[a-z]))[\u4e00-\u9fa5]+"
        match_obj = re.match(pinyin, x)
        if not (match_obj.group(1) in relat_dict):
            relat_dict[match_obj.group(1)] = x.strip(match_obj.group(1))

    if wrt_down == 1:
        """write down data to the file. nowriting is defult."""
        f = open('py_ch_relat.txt', 'w', encoding='gbk')
        f.write(str(relat_dict))
        f.close()

    os.chdir(curt_path)
    return relat_dict

def load_ch_range(range_file='一二级汉字表.txt'):
    mod_path = os.path.dirname(os.path.abspath(__file__))
    curt_path = os.getcwd()
    os.chdir(mod_path)

    f_range = open(range_file, 'r', encoding='gbk')
    range_str = f_range.read()
    f_range.close()

    os.chdir(curt_path)
    return range_str

def sort_by_value(mydict):
    """对dict进行排序"""
    myitems = mydict.items()
    backitems = [[v[1], v[0]] for v in myitems]
    backitems.sort()
    sorted_dict = dict([(backitems[i][1], backitems[i][0]) for i in range(0, len(backitems))])
    return sorted_dict

class Initmat:
    __table_name__ = 'Initial matrix'

    def __init__(self, train_str, range_str, method=2):
        self.__method = method
        self.__train_str = train_str
        self.__range_str = range_str

    def genermat(self):
        init_key = list(self.__range_str)
        init_value = list(map(lambda x: self.__train_str.count(x), self.__range_str))
        init_key_r = []
        init_value_r = []
        for i in range(len(init_value)):
            if not (init_value[i] == 0):  # 稀疏矩阵
                init_key_r.append(init_key[i])
                init_value_r.append(init_value[i])
        init_key_str = ''.join(init_key_r)
        tot_value = sum(init_value_r)
        init_value_p = [x/tot_value for x in init_value_r]
        init_dict = dict(zip(init_key_r, init_value_r))
        init_dict_p = dict(zip(init_key_r, init_value_p))
        return init_dict, init_dict_p, init_key_str

class Transmat():
    __table_name__ = 'Initial matrix'

    def __init__(self, train_str, init_dict, init_dict_p, method=2):
        self.__method = method
        self.__train_str = train_str
        self.__init_dict = init_dict
        self.__init_dict_p = init_dict_p
        self.__range_key_list = list(init_dict_p.keys())

    def genermat(self, init_key_str):
        trans_mat_dict = {}
        for x in init_key_str:  # 该在语料中出现的字符串
            later_pos = [m.start() + 1 for m in re.finditer(x, self.__train_str)]
            cut_train_list = [self.__train_str[i] for i in later_pos]
            for y in init_key_str:
                if y in cut_train_list:
                    trans_mat_dict[x + y] = cut_train_list.count(y) / self.__init_dict[x]
        return trans_mat_dict

    def calccell(self, input_str, cut_train_list, trans_mat_dict):
        if input_str in trans_mat_dict:
            return trans_mat_dict[input_str], trans_mat_dict
        trans_dict_p = 0.99 * cut_train_list.count(input_str) / self.__init_dict[input_str[0]] + \
                                              0.01 * self.__init_dict_p[input_str[0]]
        trans_mat_dict[input_str] = trans_dict_p
        return trans_dict_p, trans_mat_dict
