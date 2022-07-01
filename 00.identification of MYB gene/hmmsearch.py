#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :   00.Hmmsearch.py
@Time    :   2021/09/07 20:32:36
@Author  :   Zhangchaofan
@Version :   1.0
@Contact :   zhangchaofan22@163.com
@License :   (C)Copyright 2020-2021
@Desc    :   None
@Usage   :   python 00.Hmmsearch.py -d [pep_dir] -c [cpu_nums] -o [output_dir] -m [hmm_file]
"""
import argparse
from multiprocessing import Pool
import os
import subprocess
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
from mylog import Log

def Argparse():
    group = argparse.ArgumentParser()
    group.add_argument("-d", '--ind', help="Please input pep_dir!")
    group.add_argument("-c", '--cpus', help="Please input cpus!")
    group.add_argument('-o', '--oud', help="Please input oud!")
    group.add_argument('-m', '--hmm', help="please input the hmm_file!")
    return group.parse_args()

def dispose_onePepFile(pep):
    inf_pep = ind + pep
    species = pep.split('.')[0]
    subprocess.call('hmmsearch --domE 1E-05 -E 1E-05 %s %s  > %s%s' % (hmm, inf_pep, oud+'01.hmmsearch/', species+'.out'), shell=True)

    # get id 
    subprocess.call("awk '{if(NR>18){print $0}}' %s |  find_first_null_exit.py | awk '{print $9}' > %s" % (oud+'01.hmmsearch/'+species+'.out', oud+'02.hmm_id/'+species+'.id'), shell=True)

    # get pep
    subprocess.call('getFasta.py -i %s -l %s -o %s' % (inf_pep, oud+'02.hmm_id/'+species+'.id', oud+'03.id_pep/'+species+'.pep'), shell=True)

    # hmmscan
    subprocess.call('hmmscan --domE 1e-05 --domtblout %s /vol3/agis/chengshifeng_group/zhangchaofan/some_language_test/3.perl/zwy-perl脚本/new_test/00.dataset/Pfam-A.hmm %s' % (oud+'05.hmmscan/'+species+'.pep.domain.out', oud+'03.id_pep/'+species+'.pep'), shell=True)

    # 05.target id
    subprocess.call("hmm_get_final_pep.py -i %s -o %s -k %s" % (oud+'05.hmmscan/'+species+'.pep.domain.out', oud+'06.final_id/'+species+'.id', keyword), shell=True)

    # 06.final_pep
    subprocess.call('getFasta.py -i %s -l %s -o %s' % (oud+'03.id_pep/'+species+'.pep', oud+'06.final_id/'+species+'.id', oud+'07.final_pep/'+species+'.pep'), shell=True)

def main():
    log = Log()
    files = [i for i in os.listdir(ind) if i.endswith('.pep')]
    if not os.path.exists(oud):
        os.mkdir(oud)

    if not os.path.exists(oud+'01.hmmsearch/'):
        os.mkdir(oud+'01.hmmsearch/')

    if not os.path.exists(oud + '02.hmm_id/'):
        os.mkdir(oud + '02.hmm_id/')

    if not os.path.exists(oud + '03.id_pep'):
        os.mkdir(oud + '03.id_pep')

    if not os.path.exists(oud+ '04.nr_pep'):
        os.mkdir(oud + '04.nr_pep')

    if not os.path.exists(oud+'05.hmmscan/'):
        os.mkdir(oud + '05.hmmscan/')

    if not os.path.exists(oud+'06.final_id'):
        os.mkdir(oud + '06.final_id')

    if not os.path.exists(oud+'07.final_pep'):
        os.mkdir(oud + '07.final_pep')

    pool = Pool(processes=cpus)
    for i in files:
        log.debug("Now, Start dispose %s!" % (i))
        pool.apply_async(dispose_onePepFile, (i,))
        # dispose_onePepFile(i)
   
    pool.close()
    pool.join()

if __name__ == '__main__':
    opts = Argparse()
    ind = opts.ind 
    ind = ind if ind[-1] == '/' else ind + '/'
    cpus = int(opts.cpus)
    oud = opts.oud
    oud = oud if oud[-1] =='/' else oud + '/'
    hmm = opts.hmm
    keyword = ""
    main()
