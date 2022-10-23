#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@File    :   calc_KaKsOfGenePair.py
@Time    :   2022-02-12 21:10:30
@Author  :   Zhangchaofan
@Version :   1.0
@Contact :   zhangchaofan01@cass.cn
@License :   (C)Copyright 2022-2025
@Desc    :   None
@Usage   :   python calc_KaKsOfGenePair.py -i [raw_pep] -p [gene_pairFile] -o [output_dir] -c [cds_file]
'''
import argparse
import os
import subprocess
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
from mylog import Log
import gzip

def Argparse():
    group = argparse.ArgumentParser()
    group.add_argument("-i", '--inf', help="Please input raw_pep file!")
    group.add_argument('-p', '--pair', type=str, help="Please input the gene_paie dir!")
    group.add_argument('-o', '--oud', help="please input the output_dir!")
    group.add_argument("-c", "--cds", help="Please input the cds file!")
    return group.parse_args()


def err_exit():
    sys.exit('\033[1;31;47m!!The program exited abnormally!!\033[0m')


def seq_dic(inf):
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
                header = line.strip().replace('>', '')
            else:
                sequence += line
        else:
            break 
        line = f1.readline()
    f1.close()
    fa_dict[header] = sequence

    return fa_dict

def dispose_one(ouf, row_pep_file, pair_file, cds_file):
    # raw sequence 
    if not os.path.exists(os.path.join(ouf, '00.fa')):
        os.mkdir(os.path.join(ouf, '00.fa'))

    # MSA 
    if not os.path.exists(os.path.join(ouf, '01.MSA')):
            os.mkdir(os.path.join(ouf, '01.MSA'))
    
    # cds aln 
    if not os.path.exists(os.path.join(ouf, '02.cds_aln')):
            os.mkdir(os.path.join(ouf, '02.cds_aln'))

    # kaks value
    if not os.path.exists(os.path.join(ouf, '03.kaks')):
            os.mkdir(os.path.join(ouf, '03.kaks'))

    # 4DTV
    if not os.path.exists(os.path.join(ouf, '04.4DTV')):
            os.mkdir(os.path.join(ouf, '04.4DTV'))
    
    fa_dict = seq_dic(row_pep_file)
    cds_dic = seq_dic(cds_file)

    ## one pair for one line
    for line in open(pair_file).readlines():
        temp = line.strip().split()
        ouf_w = open(os.path.join(ouf, '00.fa', temp[0]+'-'+temp[1]+'.fa'), 'w')
        for id_order in range(len(temp)):
            if temp[id_order] not in fa_dict:
                log.debug("ERROR! %s not in raw fasta file!!!!" % (temp[id_order]))
                err_exit()
            else:
                ouf_w.write('>'+temp[id_order]+'\n'+fa_dict[temp[id_order]])
        ouf_w.close()

        # MSA
        subprocess.call("mafft --auto %s > %s 2>/dev/null" % (
            os.path.join(ouf, '00.fa', temp[0]+'-'+temp[1]+'.fa'),
            os.path.join(ouf, '01.MSA', temp[0]+'-'+temp[1]+'.MSA')
        ), shell=True)

        # find cds sequence
        cds_w= open(os.path.join(ouf, '01.MSA', temp[0]+'-'+temp[1]+'.cds'), 'w')
        cds_w.write('>'+temp[0]+'\n'+cds_dic[temp[0]] \
            + '>'+temp[1]+'\n'+cds_dic[temp[1]])
        cds_w.close()

        # pal2nal.pl
        subprocess.call("pal2nal.pl %s %s -output fasta > %s 2>/dev/null " % (
            os.path.join(ouf, '01.MSA', temp[0]+'-'+temp[1]+'.MSA'),
            os.path.join(ouf, '01.MSA', temp[0]+'-'+temp[1]+'.cds'),
            os.path.join(ouf, '02.cds_aln', temp[0]+'-'+temp[1]+'.fa')
        ), shell=True)

        # parseFastalntoAXT.pl
        subprocess.call("parseFastalntoAXT.pl %s 2>/dev/null" % (
            os.path.join(ouf, '02.cds_aln', temp[0]+'-'+temp[1]+'.fa')
        ), shell=True)

        # KaKs_Calculator 
        subprocess.call("KaKs_Calculator -i %s -o %s -m YN 2>/dev/null" % (
            os.path.join(ouf, '02.cds_aln', temp[0]+'-'+temp[1]+'.fa.axt'),
            os.path.join(ouf, '03.kaks', temp[0]+'-'+temp[1]+'.kaks')
        ), shell=True)

        # axt2_line
        subprocess.call("axt2one-line.py %s %s 2>/dev/null" % (
            os.path.join(ouf, '02.cds_aln', temp[0]+'-'+temp[1]+'.fa.axt'),
            os.path.join(ouf, '04.4DTV', temp[0]+'-'+temp[1]+'.fa.one-line'),
        ), shell=True)

        # 4DTV
        subprocess.call("calculate_4DTV_correction.pl  %s > %s  2>/dev/null" % (
            os.path.join(ouf, '04.4DTV', temp[0]+'-'+temp[1]+'.fa.one-line'),
            os.path.join(ouf, '04.4DTV', temp[0]+'-'+temp[1]+'.4dtv')
        ), shell=True)

    ##  merge
    kaks_parse = lambda line: [line.split()[i] for i in range(len(line.split())) if i in [0,2,3,4]]
    four_dtv_parse = lambda line: [line.split()[i] for i in range(len(line.split())) if i in [0,1]]
   
    kaks_tab = []
    four_tab = []
    kaks_files = ['.'.join(i.split('.')[:-1]) for i in os.listdir(os.path.join(ouf, '03.kaks')) if i.endswith("kaks")]

    for order in range(len(kaks_files)):
        kaks_line = open(os.path.join(ouf, '03.kaks', kaks_files[order]+'.kaks')).readlines()[1]
        temp = kaks_line.strip().split()[0]
        if temp != 'YN':
            # 0,2,3,4
            kaks_tab.append("\t".join(kaks_parse(kaks_line.strip())))
        if len(open(os.path.join(ouf, '04.4DTV', kaks_files[order]+'.4dtv')).readlines()) == 2:
            four_dtv = open(os.path.join(ouf, '04.4DTV', kaks_files[order]+'.4dtv')).readlines()[1]
            four_tab.append("\t".join(four_dtv_parse(four_dtv.strip())))

    # 
    kaks_w = open(os.path.join(ouf, 'all-kaks.results'), 'w')
    kaks_w.write('\n'.join(kaks_tab))
    kaks_w.close()

    #
    fourDtv_w = open(os.path.join(ouf, 'all-4dtv.results'), 'w')
    fourDtv_w.write('\n'.join(four_tab))
    fourDtv_w.close()

    # merge
    kaks_df = pd.read_csv(os.path.join(ouf, 'all-kaks.results'), header=None, sep="\t")
    kaks_df.columns = ['index', 'ka', 'ks', 'kaks']

    four_dtv = pd.read_csv(os.path.join(ouf, 'all-4dtv.results'), header=None, sep="\t")
    four_dtv.columns = ['index', '4dtv'] 

    # 
    res_df = pd.merge(kaks_df, four_dtv)
    res_df.to_csv(os.path.join(ouf, 'all.results'), sep="\t",na_rep='NA', index=None)
    
def to_run(args):
    dispose_one(args[0], args[1], args[2])

def main():
    if not os.path.exists(oud):
        os.mkdir(oud)

    arg_lst = [oud, row_pep_file, pair_file, cds_file]
    to_run(arg_lst)

    
if __name__ == '__main__':
    log = Log()
    opts = Argparse()
    row_pep_file = opts.inf
    cds_file = opts.cds
    pair_file = opts.pair
    oud = opts.oud
    main()