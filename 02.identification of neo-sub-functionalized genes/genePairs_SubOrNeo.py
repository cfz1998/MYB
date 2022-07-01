#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@File    :   genePairs_SubOrNeo.py
@Time    :   2022-04-03 15:39:26
@Author  :   Zhangchaofan
@Version :   1.0
@Contact :   zhangchaofan01@cass.cn
@License :   (C)Copyright 2022-2025
@Desc    :   None
@Usage   :   python genePairs_SubOrNeo.py -g [gene_pair] -c [reads_count from FeatureCounts result] -r [1|0 : tissue repeat > 1 or not]
'''
import argparse
import os
import subprocess
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
from mylog import Log

def err_exit():
    sys.exit('\033[1;31;47m!!The program exited abnormally, please check the log file !!\033[0m')

def Argparse():
    group = argparse.ArgumentParser()
    group.add_argument("-g", '--genP', help="Please input genePair_file!")
    group.add_argument('-c', '--count', help="Please input the RNA_count file!")
    group.add_argument('-o', '--oud', help="please input the output_dir!")
    group.add_argument('-r', '--rep', help="It's only one repeat of tissue? yes = 1 else 0",default=0)
    return group.parse_args()

def main():
    # read reads count
    total_tab = pd.read_csv(RNA_countF, sep="\t", index_col=0)

    # del Length
    if "Length" in total_tab.columns:
        total_tab = total_tab.drop("Length", axis=1)
    tissues = list(total_tab.columns)
    tissues_group = {}

    for tissue in tissues:
        # group tissue
        tmp = tissue[:-1]
        if tmp not in tissues_group:
            tissues_group[tmp] = []
        tissues_group[tmp].append(tissue)

    # get gene pair
    geneP_lines = []
    for line in open(geneP_file).readlines():
        gene1, gene2 = line.strip().split("\t")
        geneP_lines.append([gene1, gene2])

    ## create output dir
    if not os.path.exists(oud):
        os.mkdir(oud)

    if not os.path.exists(os.path.join(oud, "00.tiusse_count")):
        os.mkdir(os.path.join(oud, "00.tiusse_count"))

    ## get reads count of gene pair
    for tissue in tissues_group:
        tmp_oudW = open(os.path.join(oud, "00.tiusse_count", tissue +'.count'), 'w')
        # add header
        tissue_len = len(tissues_group[tissue])
        tmp_oudW.write("geneid\t"+"\t".join(["one"+str(x) for x in range(1, tissue_len+1)]) + \
            "\t" + "\t".join(["two"+str(x) for x in range(1, tissue_len+1)]) + "\n")
        for tmpPair in geneP_lines:
            tmp_content = '___'.join(tmpPair) + '\t'
            for tmp_gene in tmpPair:
                tmp_count = "\t".join(map(str, list(total_tab.loc[tmp_gene, tissues_group[tissue]])))
                tmp_content += tmp_count + "\t"
            tmp_oudW.write(tmp_content.strip() + "\n")

        tmp_oudW.close()

    # 
    if not os.path.exists(os.path.join(oud, "01.edgeR_res")):
        os.mkdir(os.path.join(oud, "01.edgeR_res"))

    for tissue in tissues_group:
        if rep:
            subprocess.call("EdgeR_OneRepeat.R %s %s" % (
                os.path.join(oud, "00.tiusse_count", tissue +'.count'),
                os.path.join(oud, "01.edgeR_res", tissue+'.edgeR.txt')    
            ), shell=True)

		
        else:
            subprocess.call("EdgeR.R %s %s" % (
                os.path.join(oud, "00.tiusse_count", tissue +'.count'),
                os.path.join(oud, "01.edgeR_res", tissue+'.edgeR.txt')
            ), shell=True)

    #
    edgeR_tab = {}
    for tissue in tissues_group:
        tmp_df = pd.read_csv(os.path.join(oud, "01.edgeR_res", tissue+'.edgeR.txt'), sep="\t", 
            skiprows=1, names = ["logFC", "logCPM",     "PValue", "FDR"], index_col=0)
        for tmpPair in geneP_lines:
            tmp_id = '___'.join(tmpPair)
            if tmp_id not in edgeR_tab:
                edgeR_tab[tmp_id] = []
            if tmp_id in tmp_df.index:
                tmp_LogFC = float(tmp_df.loc[tmp_id, "logFC"])
                if tmp_LogFC > 1:
                    edgeR_tab[tmp_id].append('up')
                elif tmp_LogFC < -1:
                    edgeR_tab[tmp_id].append('down')
                else:
                    edgeR_tab[tmp_id].append('nodiff')
            else:
                edgeR_tab[tmp_id].append('NA')

    # output result
    oud_w = open(os.path.join(oud, "final_res.txt"), "w")
    oud_w.write("geneid1\tgeneid2\t"+"\t".join(tissues_group.keys())+"\tann\n")
    for tmpPair in geneP_lines:
        tmp_lst = edgeR_tab['___'.join(tmpPair)]
        up = tmp_lst.count('up')
        down = tmp_lst.count('down')
        if up > 0 and down > 0:
            oud_w.write("\t".join(tmpPair)+"\t" + "\t".join(map(str, tmp_lst))+"\tsub\n")
        elif (up >= len(tissues_group) / 3 and down == 0) or (down >= len(tissues_group) / 3 and up == 0):
            oud_w.write("\t".join(tmpPair)+"\t" + "\t".join(map(str, tmp_lst))+"\tAED\n")
        else:
            oud_w.write("\t".join(tmpPair)+"\t" + "\t".join(map(str, tmp_lst))+"\tnodiff\n")

    oud_w.close()

if __name__ == '__main__':
    log = Log()
    opts = Argparse()
    geneP_file = opts.genP
    RNA_countF = opts.count
    oud = opts.oud
    rep = opts.rep
    main()
