import sys

# commandline: python get_taxa.py alignments.sam

fullnamelineage,taxaid2name = {},{}

for i in open('/lustre/projects/SethCommichaux/MTDNA/taxa_info/fullnamelineage.dmp'):
	tmp = map(lambda x:x.strip('\t|'), i.strip().split('\t|\t'))
	taxid = tmp[0]
	taxaName = tmp[1].upper()
	lineage = tmp[2]
	fullnamelineage[taxid] = lineage
	taxaid2name[taxid] = taxaName

read_count = int(sys.argv[2])
results,uniqueness = {},{}


def checkTaxaName(taxa_id):
	if taxa_id not in fullnamelineage:
		return False
	else:
		return taxa_id


for i in open(sys.argv[1]):
	if i.startswith('@'):
		continue
	else:
		read = i.strip().split('\t')[0]
		taxaid = i.strip().split('\t')[2]
		if read in uniqueness:
			taxa = checkTaxaName(taxa)
			if taxa == False:
				continue
			x = fullnamelineage.get(taxa)+taxaid2name[taxa]
			x = x.split(';')
			tmp = uniqueness[read].split(';')
			new_lineage = []
			for t in range(min(len(x),len(tmp))):
				if x[t] == tmp[t]:
					new_lineage.append(x[t])
				elif x[t] != tmp[t]:
					uniqueness[read] = ';'.join(new_lineage)
					break
			else:
				uniqueness[read] = ';'.join(new_lineage)
		else:
			taxa = checkTaxaName(taxa)
			if taxa == False:
				continue
			uniqueness[read] = fullnamelineage.get(taxa)+taxaid2name[taxa]



no_double_count = {}


for i in open(sys.argv[1]):
	if i.startswith('@'):
		continue
	else:
		tmp = i.strip().split('\t')
		read = tmp[0]
		if read not in uniqueness:
			continue
		if read in no_double_count:
			continue
		no_double_count[read] = 0
		taxa = uniqueness[read]
		position = int(tmp[3])
		seq = len(tmp[9])
		if taxa not in results:
			results[taxa] = 1
		else:
			results[taxa] += 1


with open(sys.argv[1]+'.results','a') as out:
	for k,v in sorted(results.items(),key=lambda x: x[1]):
		out.write(str(k)+'\t'+str(v)+'\t'+str(float(v)/read_count)+'\n')

