### identification of MYB gene

#### 1. getFasta.py

> Get sequence from fasta file.  
> Usage: python getFasta.py species.pep gene_lst gene_fa

#### 2. hmm_get_final_pep.py

> get target ID from hmmscan result
> Usage: python hmm_get_final_pep.py -i [hmm_ouf] -o [pep_id] -k [domain_name]

#### 3. hmmsearch.py

> Identification MYB gene from protein sequences  
> python 00.Hmmsearch.py -d [pep_dir] -c [cpu_nums] -o [output_dir] -m [hmm_file]
