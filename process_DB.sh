#!/bin/sh
#$ -N process_DB
#$ -j y
#$ -pe mpi 18
#$ -cwd

module load prokka biopython bowtie/2.3.1/bowtie blast

cat Rickettsia_prowazekii.fasta mtDNA_refseq_wga_taxa.fasta > x; mv x mtDNA_refseq_wga_taxa.fasta
cat Gloeomargarita_lithophora.fasta plastid_refseq_wga_taxa.fasta > x; mv x plastid_refseq_wga_taxa.fasta

python reformat_fasta_to_taxaFasta.py mtDNA_genbank_taxa.fasta mtDNA_refseq_wga_taxa.fasta all_mtDNA.fasta
python reformat_fasta_to_taxaFasta.py plastid_genbank_taxa.fasta plastid_refseq_wga_taxa.fasta all_plastid.fasta

bowtie2-build-l --threads 18 all_mtDNA.fasta all_mtDNA
bowtie2-build-l --threads 18 all_plastid.fasta all_plastid

makeblastdb -in all_mtDNA.fasta -out all_mtDNA -dbtype nucl
makeblastdb -in all_plastid.fasta -out all_plastid -dbtype nucl

prokka --outdir all_mtDNA_prokka --prefix all_mtDNA --kingdom Mitochondria --gcode 4 --cpus 18 all_mtDNA.fasta
prokka --outdir all_plastid_prokka --prefix all_plastid --gcode 11 --cpus 18 all_plastid.fasta

