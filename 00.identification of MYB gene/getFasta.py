#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :   getFasta.py
@Time    :   2021/11/15 13:34:03
@Author  :   Zhangchaofan
@Version :   1.0
@Contact :   zhangchaofan01@cass.cn
@License :   (C)Copyright 2020-2021
@Desc    :   Get gene sequence from fasta file.
@Usage   :   python getFasta.py species.pep gene_lst gene_fa
"""
import argparse
import gzip
import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
from mylog import Log

def Argparse():
    group = argparse.ArgumentParser()
    group.add_argument('-i', '--inf',help="Please input the speciesTotalseq!")
    group.add_argument('-l', '--list', help="Please input the target list!")
    group.add_argument('-o', '--ouf',help="Please input the ouf_file!")
    return group.parse_args()

def main():

    f1 = gzip.open(inf, 'rt') if inf.endswith('gz') else open(inf)
    line = f1.readline()
    sequence = ""
    fa_dict = {}
    while True:
        if line:
            if line[0] == '>':
                if len(sequence) > 0:
                    fa_dict[header] = sequence
                    sequence = ""
                header = line.strip()
            else:
                sequence += line
        else:
            break
        line = f1.readline()
    f1.close()

    if header not in fa_dict:
        fa_dict[header] = sequence    

    f1 = open(list_)
    ouf_w = open(ouf, 'w')
    line = f1.readline()
    while True:
        if line:
            line = '>' + line.strip()
            if line in fa_dict:
                ouf_w.write(line+'\n'+fa_dict[line])
            else:
                log.error("%s Not in raw_pep file!" % (line))
        else:
            break
        line = f1.readline()
        
    f1.close()
    ouf_w.close()

if __name__ == '__main__':
    log = Log()
    opts = Argparse()
    inf = opts.inf
    list_ = opts.list
    ouf = opts.ouf
    main()