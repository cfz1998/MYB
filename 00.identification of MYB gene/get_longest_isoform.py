#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :   get_longest_isoform.py
@Time    :   2021/09/01 9:32:36
@Author  :   Zhangchaofan
@Version :   1.0
@Contact :   zhangchaofan22@163.com
@License :   (C)Copyright 2020-2021
@Desc    :   None
@Usage   :   python get_longest_isoform.py [raw_peptide] [longest_isoform]
"""
from sys import argv
import gzip
import os

def readFasta(fastaFile):
    f1 = gzip.open(fastaFile, 'rt') if fastaFile.endswith('gz') else open(fastaFile)
    line = f1.readline()
    sequence = ""
    fasta_dict = {}
    header = ""
    while True:
        if line:
            if line[0] == '>':
                if len(sequence) > 0:
                    fasta_dict[header] = sequence
                    sequence = ""
                # split()[0] may be change
                header = line.strip().replace('>', '').split()[0]
            else:
                sequence += line.strip()
        else:
            break
        line = f1.readline()
    f1.close()
    if header and sequence:
        fasta_dict[header] = sequence

    return fasta_dict

def main():
    raw_pep_dic = readFasta(argv[1])
    gene_seq_dic = {}
    for isoform_id in raw_pep_dic:
        # split(".")[0] depends on actually id feature
        # may change it. like split("-")[0]
        # or depends on gff file for ncbi genome datas
        gene_name = isoform_id.split(".")[0]
        if gene_name not in gene_seq_dic:
            gene_seq_dic[gene_name] = [isoform_id, raw_pep_dic[isoform_id]]
        else:
            if len(raw_pep_dic[raw_pep_dic]) > gene_seq_dic[gene_name][1]:
                gene_seq_dic[gene_name] = [isoform_id, raw_pep_dic[isoform_id]]

    ouf_w = open(argv[2], 'w')
    for gene_name in gene_seq_dic:
        ## normalize node names if required
        # species_name = os.path.basename(argv[1]).split('.')[0]
        # ouf_w.write(">"+species_name+"|"gene_seq_dic[gene_name][0]+"\n"+gene_seq_dic[gene_name][1]+"\n")
        ouf_w.write(">"+gene_seq_dic[gene_name][0]+"\n"+gene_seq_dic[gene_name][1]+"\n")

    ouf_w.close()

main()
