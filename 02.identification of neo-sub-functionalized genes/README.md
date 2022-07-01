### identification of neo-sub-functionalized genes

#### RNA-seq pipeline

```python
# hisat2
hisat2 -x genome_index -p 4 -1 fastq1 -2 fastq1 -S sra.sam &> sra.log

# sam -> bam
samtools view -bS -@ 4 sra.sam > sra.bam

# featureCounts
featureCounts -T 4 -p -t feature-type -g gene_id -a GTF -o sra.txt sra.bam &>> sra,log

# cout
cut -f 1,6,7 sra.txt |grep -v '^#' > sra.count

```

#### 1. genePairs_SubOrNeo.py

> Get expression pattern of MYB pairs.  
> python genePairs_SubOrNeo.py -g [gene_pair] -c [reads_count from FeatureCounts result] -r [1|0 : tissue repeat > 1 or not]

#### 2. EdgeR.R

> This script to differential expression analysis.  
> This script is used in conjunction with genePairs_SubOrNeo.py.

#### 3. EdgeR_OneRepeat.R

> Use it when repeating a singl.
