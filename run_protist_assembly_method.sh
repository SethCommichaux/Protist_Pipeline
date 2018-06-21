#!/bin/bash

#$ -N spades
#$ -j y
#$ -S /bin/bash
#$ -pe mpi 10
#$ -cwd
# Authors: Seth Commichaux <Seth.Commichaux@fda.hhs.gov>

shopt -s extglob

module load muscle FastTree spades prokka blast biopython

for i in *fastq.gz;
do

spades.py --only-assembler --12 $i -o $i.spades --meta -t 10;

prokka --kingdom Mitochondria --rnammer --outdir $i.spades/$i.prokka --cpus 10 --prefix ${i%.fastq.gz} --locus ${i%.fastq.gz} $i.spades/contigs.fasta;

blastn -query $i.spades/$i.prokka/${i%fastq.gz}ffn -db /lustre/projects/SethCommichaux/MTDNA/Sara_Handy/all_CDS -evalue 0.00001 -outfmt "6 qaccver saccver pident length evalue slen" -num_threads 10 | awk -F "\t" '$4/$6 > 0.5 {print $0}' >> $i.spades/$i.prokka/$i.blast;

python get_tree_blast.py $i.spades/$i.prokka/$i.blast $i.spades/$i.prokka/${i%fastq.gz}ffn;

done

