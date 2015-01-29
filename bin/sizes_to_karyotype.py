#!/hive/groups/recon/local/bin/python
import sys
import re

old_prefix = 'scaffold|C'
#old_prefix = 'chr'
prefix = 'pt'
#prefix = 'fc'
def load_synteny_blocks(synteny_file) :
    synteny_blocks = []
    with open(synteny_file) as f:
        for line in f:
            data = line.strip().split()
            synteny_blocks.append(data)
    return synteny_blocks

input = sys.argv[1]
output = sys.argv[2]
synteny_file = sys.argv[3]
synteny_blocks = load_synteny_blocks(synteny_file)
#names = map(lambda x: x[1].split(prefix)[1] if prefix in x[1] else x[5].split(prefix)[1], synteny_blocks)
with open(input) as inp:
    with open(output,'w') as out:
        for line in inp:
            line = line.strip()
            data = line.split()
            id = [s.strip() for s in re.split(old_prefix, data[0])][1]
            #if id in names:
            out.write('chr - ' + prefix + id + ' ' + prefix + id + ' 0 '+ data[1] + ' ' + prefix + id +'\n')
