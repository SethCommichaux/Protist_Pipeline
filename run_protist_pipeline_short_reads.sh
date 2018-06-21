#!/bin/sh
#$ -N bowtie_genomes
#$ -j y
#$ -pe mpi 12
#$ -cwd

module load bowtie/2.2.9/bowtie biopython
module load sratoolkit

shopt -s extglob

while read i;
do echo $i;

fastq-dump $i

x=$(grep -c '^+' $i.fastq)

bowtie2-align-l -a -p 12 --no-unal --end-to-end -x /lustre/projects/SethCommichaux/MTDNA/Protist_pipeline_scripts_DB/all_mtDNA -U $i.fastq -S $i.mt.sam;
bowtie2-align-l -a -p 12 --no-unal --end-to-end -x /lustre/projects/SethCommichaux/MTDNA/Protist_pipeline_scripts_DB/plastid_refseq_wga_taxa -U $i.fastq -S $i.plastid.sam;

python /lustre/projects/SethCommichaux/MTDNA/Protist_pipeline_scripts_DB/get_taxa_short_reads.py $i.mt.sam $x;
python /lustre/projects/SethCommichaux/MTDNA/Protist_pipeline_scripts_DB/get_taxa_short_reads.py $i.plastid.sam $x

grep -vi 'Metazoa' $i.mt.sam.results | grep -vi 'Embryophy' | grep -vi 'fungi' | sort > $i.mt.sam.results.protist;
grep -vi 'Metazoa' $i.plastid.sam.results | grep -vi 'Embryophy' | grep -vi 'fungi' |sort > $i.plastid.sam.results.protist;

python /lustre/projects/SethCommichaux/MTDNA/Protist_pipeline_scripts_DB/get_groups_short_reads.py $i.mt.sam.results.protist /lustre/projects/SethCommichaux/MTDNA/taxa_info/fullnamelineage.dmp /lustre/projects/SethCommichaux/MTDNA/taxa_info/nodes.dmp $x;
python /lustre/projects/SethCommichaux/MTDNA/Protist_pipeline_scripts_DB/get_groups_short_reads.py $i.plastid.sam.results.protist /lustre/projects/SethCommichaux/MTDNA/taxa_info/fullnamelineage.dmp /lustre/projects/SethCommichaux/MTDNA/taxa_info/nodes.dmp $x;

done < SRA.txt
