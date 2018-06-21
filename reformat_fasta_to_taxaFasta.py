import sys
from Bio import SeqIO

fullnamelineage = {i.strip().split('\t|\t')[1].upper():i.strip().split('\t|\t')[2].strip('\t|') for i in open('/lustre/projects/SethCommichaux/MTDNA/taxa_info/fullnamelineage.dmp')}
results = {}

for i in SeqIO.parse(sys.argv[1],'fasta'):
                tmp = str(i.description).upper()
                candidates = []
                for k in fullnamelineage.keys():
                        if k in tmp:
                                candidates.append(k)
                if candidates == []:
                        continue
                candidates = sorted(candidates,key=len)[-1]
                results[candidates] = str(i.seq)


with open(sys.argv[1].replace('.fasta','_taxa.fasta'),'w') as out:
        for k,v in results.items():
                out.write('>'+k.replace(' ','_')+'\n'+v+'\n')

