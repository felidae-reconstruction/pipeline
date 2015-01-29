#!/hive/groups/recon/local/bin/python
#filter synteny blocks for those that correspond to a single scaffold

import sys
from collections import Counter
import re

old_prefix1 = 'C'
old_prefix2 = 'KN|JPTV'
prefix1 = 'C'
prefix2 = 'KN'

def parse_blocks(input):
    blocks = []
    with open(input) as f:
        for line in f:
            line = line.strip()
            if '#' in line:
                continue
            data = line.split()
            blocks.append(data)
    return blocks
            

def filter_scaffolds(blocks):
    not_unique_scaffolds = []
    #for i in [1,5] :
    for i in [1] :
        scaffolds = [x[i] for x in blocks]
        c = Counter(scaffolds)
        not_unique_scaffolds += filter(lambda x:c[x] > 1, scaffolds)
    return set(not_unique_scaffolds)

def get_largest_translocations(blocks, not_unique_scaffolds, n=10):
    filtered_blocks = []
    for e in blocks:
        if e[1] in not_unique_scaffolds:
            filtered_blocks.append(e)
    names = map(lambda x: x[1], filtered_blocks)
    lengths = []
    for name in set(names) :
        name_blocks = filter(lambda x: x[1] == name, filtered_blocks)
        length = sum([int(x[3]) for x in name_blocks])
        lengths.append((name,length))
    lengths = sorted(lengths, key=lambda x:x[1], reverse=True)
    return dict(lengths[:n]).keys()

def output_for_circos(blocks, filtered_names, file_name):
    with open(file_name,'w') as f:
        for e in blocks:
            if not e[1] in filtered_names: #or not e[1] in not_unique_scaffolds:
                continue
            #id1 = [s.strip() for s in re.split(old_prefix1, e[1])][1]
            #name1 = prefix1 + id1
            #id2 = [s.strip() for s in re.split(old_prefix2, e[5])][1]
            #name2 = prefix2 + id2
            name1 = e[1]
            name2 = e[5]
            if e[4] == '+':
                start1 = int(e[2])
                end1 = int(e[2]) + int(e[3])
            else :
                start1 = int(e[2]) + int(e[3])
                end1 = int(e[2])
            if e[8] == '+':
                start2 = int(e[6])
                end2 = int(e[6]) + int(e[7])
            else :
                start2 = int(e[6]) + int(e[7]) 
                end2 = int(e[6])
            f.write(name1 + ' ' + str(start1) + ' ' + str(end1) + ' ' + name2 + ' ' + str(start2) + ' ' + str(end2)+ '\n')  

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE:', sys.argv[0], 'blocks.txt', 'output.txt'
        exit()
    input = sys.argv[1]
    output = sys.argv[2]
    blocks = parse_blocks(input)
    not_unique_scaffolds = filter_scaffolds(blocks)
#get top 10 rearrangements by length
    filtered_names = get_largest_translocations(blocks, not_unique_scaffolds)
    output_for_circos(blocks, filtered_names, output)
    #output_for_circos(blocks, not_unique_scaffolds, output)
