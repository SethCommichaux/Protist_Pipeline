import sys,os
from Bio import SeqIO

path = '/lustre/projects/SethCommichaux/MTDNA/Sara_Handy/'
path1 = '/lustre/projects/SethCommichaux/MTDNA/protist_basal_eukaryotes_alphaproteobacteria_reference/WGA/cluster_seqs/'

f = sys.argv[1]
f2 = {str(i.id):str(i.seq) for i in SeqIO.parse(sys.argv[2],'fasta')}

def find_cluster(x):
        print x
        fs = os.listdir('/lustre/projects/SethCommichaux/MTDNA/protist_basal_eukaryotes_alphaproteobacteria_reference/WGA/cluster_seqs/')
        for i in fs:
                if i.endswith('.fasta')== False:
                        continue
                clusters = {}
                for j in SeqIO.parse(path1+i,'fasta'):
                        clusters['_'.join(str(j.description).split('_')[:-1])] = str(j.seq)
                if x in clusters:
                        print i
                        return i

for h,i in enumerate(open(f)):
        tmp = i.strip().split('\t')
        qaccver,saccver,pident,length,evalue,slen = tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5]
        cluster = find_cluster(saccver)
        with open(f+'_blast'+str(h),'w') as out:
                out.write('>'+qaccver+'\n'+f2[qaccver]+'\n')
        os.system('cat '+f+'_blast'+str(h)+' '+path1+cluster+' > '+qaccver+'; rm '+f+'_blast'+str(h))
        os.system('muscle -in '+qaccver+' -out '+f+'_blast'+str(h)+'.aln; FastTree -slow -boot 1000 -nt '+f+'_blast'+str(h)+'.aln > '+f+'_blast'+str(h)+'.tree; rm '+qaccver)

