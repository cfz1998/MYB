#!/public/home/zhangchaofan/anaconda3/bin/python
# -*- coding: utf-8 -*-
'''
@File    :   orthofinder_genePairs.py
@Time    :   2022-01-05 22:43:01
@Author  :   Zhangchaofan
@Version :   1.0
@Contact :   zhangchaofan22@163.com
@License :   (C)Copyright 2020-2021
@Desc    :   None
@Usage   :   
'''
import argparse
from multiprocessing import Pool
import os
from re import T
import subprocess
import sys
import pandas as pd
from mylog import Log

def err_exit():
    sys.exit('\033[1;31;47m!!The program exited abnormally!\033[0m')

def Argparse():
    group = argparse.ArgumentParser()
    group.add_argument("-i", '--inf', help="Please input Duplications.tsv!")
    group.add_argument('-o', '--oud', help="please input the output_dir!")
    return group.parse_args()

def one_ortho(inf):
    DUP_dic = {}
    OG_order = []
    for line in open(inf).readlines()[1:]:
        temp = line.strip().split("\t")
        if temp[0] not in DUP_dic:
            DUP_dic[temp[0]] = {}
            OG_order.append(temp[0])

        gene1 = temp[-2].strip().split(',')
        gene2 = temp[-1].strip().split(',')
        genes = gene1 + gene2

        for gene in genes:
            gene = gene.strip()
            #
            if gene.count('_') > 2:
                species = '_'.join(gene.split('_')[:-1])
            else:
                species = gene.split('_')[0]

            if species not in DUP_dic[temp[0]]:
                DUP_dic[temp[0]][species] = []

            if gene not in DUP_dic[temp[0]][species]:
                DUP_dic[temp[0]][species].append(gene)


    for OG in OG_order:
        if DUP_dic[OG]:
            for species in DUP_dic[OG]:
                spe_name = species 
                ouf_w = open(os.path.join(oud, spe_name+'.txt'), 'a+')
                ouf_w.write('\t'.join(DUP_dic[OG][species])+'\n')
                ouf_w.close()

def main():    
    if not os.path.exists(oud):
        os.mkdir(os.mkdir(oud))

    one_ortho(inf)


if __name__ == '__main__':
    log = Log()
    opts = Argparse()
    inf = opts.inf
    oud = opts.oud
    main()
