import sys

# commandline: python get_taxa_long_read.py results.blast.txt read_count

fullnamelineage = {i.strip().split('\t|\t')[1].upper():i.strip().split('\t|\t')[2].strip('\t|') for i in open('/lustre/projects/SethCommichaux/MTDNA/taxa_info/fullnamelineage.dmp')}
read_count = int(sys.argv[2])
results,uniqueness = {},{}

def checkTaxaName(taxa_name):
        if taxa_name not in fullnamelineage:
                taxa_name = taxa_name.split(' ')[0]
                if taxa_name not in fullnamelineage:
                        return False
                else:
                        return fullnamelineage[taxa_name]
        else:
                return fullnamelineage[taxa_name]


for i in open(sys.argv[1]):
        tmp = i.strip().split('\t')
        read,taxa,qlen,start,stop,bitscore = tmp[0],tmp[1],int(tmp[-1]),int(tmp[6]),int(tmp[7]),float(tmp[-2])
        if read not in uniqueness:
                uniqueness[read] = {taxa:[bitscore,range(start,stop),qlen]}
        else:
                if taxa in uniqueness[read]:
                        uniqueness[read][taxa][0] += bitscore
                        uniqueness[read][taxa][1] += range(start,stop)
                        uniqueness[read][taxa][1] = list(set(uniqueness[read][taxa][1]))
                else:
                        uniqueness[read][taxa] = [bitscore,range(start,stop),qlen]

for k,v in uniqueness.items():
        for z,w in v.items():
                uniqueness[k][z][1] = len(uniqueness[k][z][1])
                if uniqueness[k][z][1] < 0.5*uniqueness[k][z][2]:
                        uniqueness[k].pop(z)
        if v == {}:
                uniqueness.pop(k)

for k,v in uniqueness.items():
        scoring,new_lineage = 0,''
        for z,w in v.items():
                scoring = max(uniqueness[k][z][0],scoring)
        for z,w in v.items():
                if uniqueness[k][z][0] < scoring:
                        uniqueness[k].pop(z)
                else:
                        z = z.replace('_',' ').upper()
                        taxa = checkTaxaName(z)
                        if taxa == False:
                                continue
                        else:
                                x = taxa+z
                                if new_lineage == '':
                                        new_lineage = x
                                else:
                                        x = x.split(';')
                                        new_lineage = new_lineage.split(';')
                                        tmp = []
                                        for t in range(min(len(x),len(new_lineage))):
                                                if x[t] == new_lineage[t]:
                                                        tmp.append(x[t])
                                                elif x[t] != new_lineage[t]:
                                                        break
                                        new_lineage = ';'.join(tmp)
        if new_lineage in results:
                results[new_lineage] += 1
        else:
                results[new_lineage] = 1


with open(sys.argv[1]+'.results','w') as out:
        for k,v in sorted(results.items(),key=lambda x: x[1]):
                out.write(str(k)+'\t'+str(v)+'\t'+str(float(v)/read_count)+'\n')

