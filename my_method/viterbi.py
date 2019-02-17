#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" viterbi method """

__author__ = 'Shen Lei'

import os
import re

def viterbi(pinyin_list, relat_dict, init_dict_p, trans_mat_dict):
    """
     input: pinyin_list (list): 拼音列表
     output: ch_list: 汉字列表
    """
    def sort_by_value(mydict):
        """对dict进行排序"""
        myitems = mydict.items()
        backitems = [[v[1], v[0]] for v in myitems]
        backitems.sort(reverse=True)
        sorted_dict = dict([(backitems[i][1], backitems[i][0]) for i in range(0, len(backitems))])
        return sorted_dict

    min_ch = min(list(init_dict_p.values()))
    prob_list_1 = list(relat_dict[pinyin_list[0]])
    prob_value = list(map(lambda x: init_dict_p.get(x, min_ch), prob_list_1))  # 句首汉字概率平滑操作
    V = dict(zip(prob_list_1, prob_value))

    if len(pinyin_list) < 2:
        sorted_V = sort_by_value(V)
        output_ch_str = list(sorted_V.keys())[0] + '\n'
        return output_ch_str

    for i in range(1, len(pinyin_list)):
        py_later_str = pinyin_list[i]
        ch_later_str = relat_dict[py_later_str]
        prob_map = {}
        for j in ch_later_str:
            """viterbi算法实现"""
            max_list = []
            max_prob = 0
            for phrase, first_prob in V.items():
                first_ch = phrase[-1]
                comb_ch = first_ch + j
                new_prob = trans_mat_dict.get(comb_ch, init_dict_p.get(first_ch, min_ch)/100)  #条件概率平滑操作
                new_prob = new_prob * first_prob
                if new_prob > max_prob:
                    max_prob = new_prob
                    max_list = phrase + j
                if max_prob == 0:
                    continue
            prob_map[max_list] = max_prob
        V = prob_map
    sorted_V = sort_by_value(V)
    output_ch_str = list(sorted_V.keys())[0] + '\n'
    return output_ch_str