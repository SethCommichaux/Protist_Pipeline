#!/bin/sh
#$ -N pacbio
#$ -j y
#$ -pe mpi 12
#$ -cwd

module load blast sratoolkit

shopt -s extglob

while read i;
do echo $i;

fastq-dump --fasta $i;

x=$(grep -c '^>' $i.fasta)
echo $x

blastn -query $i.fasta -db /lustre/projects/SethCommichaux/MTDNA/Protist_pipeline_scripts_DB/all_mtDNA -evalue 0.00001 -outfmt "6 qaccver saccver pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen" -out $i.mt.blast -num_threads 12
blastn -query $i.fasta -db /lustre/projects/SethCommichaux/MTDNA/Protist_pipeline_scripts_DB/plastid_refseq_wga_taxa -evalue 0.00001 -outfmt "6 qaccver saccver pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen" -out $i.plastid.blast -num_threads 12

python get_taxa_long_read.py $i.mt.blast $x;
python get_taxa_long_read.py $i.plastid.blast $x

grep -vi 'Metazoa' $i.mt.blast.results | grep -vi 'Embryophy' | grep -vi 'fungi' | sort > $i.mt.blast.results.protist;
grep -vi 'Metazoa' $i.plastid.blast.results | grep -vi 'Embryophy' | grep -vi 'fungi' |sort > $i.plastid.blast.results.protist;

python get_groups_long_read.py $i.mt.blast.results.protist /lustre/projects/SethCommichaux/MTDNA/taxa_info/fullnamelineage.dmp /lustre/projects/SethCommichaux/MTDNA/taxa_info/nodes.dmp $x;
python get_groups_long_read.py $i.plastid.blast.results.protist /lustre/projects/SethCommichaux/MTDNA/taxa_info/fullnamelineage.dmp /lustre/projects/SethCommichaux/MTDNA/taxa_info/nodes.dmp $x;

done < SRA.txt
