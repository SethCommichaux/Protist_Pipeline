#python get_groups.py *.protist /path/to/fullnamelineage.dmp /path/to/nodes.dmp read_count
import sys

name2taxid = {i.split("\t|\t")[1].upper():i.split("\t|\t")[0] for i in open(sys.argv[2])}
taxid2taxaGroup = {i.split("\t|\t")[0]:i.split("\t|\t")[2] for i in open(sys.argv[3])}

results = {}

for i in open(sys.argv[1]):
        tmp = i.strip().split('\t')
        lineage = map(lambda x:x.strip(),tmp[0].strip().split(';'))
        genus,species = 0,0
        g,s = 0,0
        counts = int(tmp[1])
        proportions = float(tmp[2])
        for j in lineage:
                try:
                        if taxid2taxaGroup[name2taxid[j]].upper() == 'GENUS':
                                genus = counts
                                g = j
                        if taxid2taxaGroup[name2taxid[j]].upper() == 'SPECIES':
                                species = counts
                                s = j
                except KeyError:
                        continue
        try:
                pos = lineage.index('Eukaryota')
                if pos != len(lineage) - 1:
                        major_protist_group = lineage[pos+1]
                        if major_protist_group not in results:
                                results[major_protist_group] = [counts,genus,species,[g],[s]]
                        else:
                                results[major_protist_group][0] += counts
                                results[major_protist_group][1] += genus
                                results[major_protist_group][2] += species
                                results[major_protist_group][3].append(g)
                                results[major_protist_group][4].append(s)
        except ValueError:
                continue


with open(sys.argv[1]+'.groups','w') as out:
        out.write('Major_protist_group\tMajor_group_read_count\tMajor_group_proportion_reads\tReads_assigned_genus\tReads_assigned_species\tReads_unknown_nonspecific\tGenera_found\tSpecies_found\n')
        for k,v in results.items():
                x = list(set([i for i in v[3] if i != 0]))
                y = list(set([i for i in v[4] if i != 0]))
                out.write(k+'\t'+str(v[0])+'\t'+str(v[0]/float(sys.argv[4]))+'\t'+str(v[1])+'\t'+str(v[2])+'\t'+str(v[0]-v[1]-v[2])+'\t'+str(x)+'\t'+str(y)+'\n')

