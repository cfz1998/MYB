#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@File    :   hmm_get_final_pep.py
@Time    :   2022-02-12 13:02:06
@Author  :   Zhangchaofan
@Version :   1.0
@Contact :   zhangchaofan22@163.com
@License :   (C)Copyright 2022-2025
@Desc    :   None
@Usage   :   python hmm_get_final_pep.py -i [hmm_ouf] -o [pep_id] -k [domain_name]
'''
import argparse
from multiprocessing import Pool
import os
import subprocess
import sys
import pandas as pd

def err_exit():
    sys.exit('\033[1;31;47m!!The program exited abnormally!!\033[0m')

def Argparse():
    group = argparse.ArgumentParser()
    group.add_argument("-i", '--inf', help="Please input input_file!")
    group.add_argument('-o', '--ouf', help="please input the output_file!")
    group.add_argument('-k', '--keyword', help="please input the keyword!")
    return group.parse_args()


def main():
    pep_lst = []
    
    for line in open(inf).readlines():
        temp = line.strip().split()
        # 这个 == "" 里面要改改
        if temp[0] == keyword and temp[3] not in pep_lst:
            pep_lst.append(temp[3])

    ouf_w = open(ouf, 'w')
    ouf_w.write('\n'.join(pep_lst))

if __name__ == '__main__':
    opts = Argparse()
    inf = opts.inf
    ouf = opts.ouf
    keyword = opts.keyword
    main()
    
