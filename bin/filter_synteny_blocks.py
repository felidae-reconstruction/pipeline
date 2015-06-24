#!/hive/groups/recon/local/bin/python
#filter synteny blocks for those that correspond to a single scaffold

import sys
from collections import Counter
import re
import argparse

#old_prefix1 = 'C'
#old_prefix2 = 'KN|JPTV'
#prefix1 = 'C'
#prefix2 = 'KN'

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
    #find not unique scaffolds for the second specie
    for i in [1,5] :
        scaffolds = [x[i] for x in blocks]
        c = Counter(scaffolds)
        not_unique_scaffolds += filter(lambda x:c[x] > 1, scaffolds)
    return set(not_unique_scaffolds)

#translocation order (so called size) equals to lengths of all synteny blocks of the rearranged scaffold
def get_largest_translocations(blocks, not_unique_scaffolds, n=10):
    filtered_blocks = []
    for e in blocks:
        #choose 1 or 5 - depending on species order in block file
        if e[5] in not_unique_scaffolds:
            filtered_blocks.append(e)
    names = map(lambda x: x[5], filtered_blocks)
    lengths = []
    for name in set(names) :
        name_blocks = filter(lambda x: x[5] == name, filtered_blocks)
        length = sum([int(x[7]) for x in name_blocks])
        lengths.append((name,length))
    lengths = sorted(lengths, key=lambda x:x[1], reverse=True)
    print lengths
    #print 'number of scaffolds translocated', len(lengths)
    for e in lengths:
        chrs = map(lambda x: x[1], filter(lambda x: x[5] == e[0],blocks))
        #print e[0], chrs, e[1]
    return dict(lengths[:n]).keys()

def output(blocks, filtered_names, file_name):
    with open(file_name,'w') as f:
        for e in blocks:
            if not e[5] in filtered_names: 
                continue
            f.write(' '.join(e)+'\n')

def output_for_circos(blocks, filtered_names, file_name):
    with open(file_name,'w') as f:
        for e in blocks:
            #e[1] or e[5] dependent on species order
            if not e[5] in filtered_names: #or not e[1] in not_unique_scaffolds:
                continue
            name1 = e[1]
            name2 = e[5]
            start1 = int(e[2])
            end1 = int(e[2]) + int(e[3])
            start2 = int(e[6])
            end2 = int(e[6]) + int(e[7]) 
            '''
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
            '''
            f.write(name1 + ' ' + str(start1) + ' ' + str(end1) + ' ' + name2 + ' ' + str(start2) + ' ' + str(end2)+ '\n')  

if __name__ == '__main__':
    print 'Note that all the calculations are performed for the second specie!'
    print
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    blocks = parse_blocks(args.input)
    not_unique_scaffolds = filter_scaffolds(blocks)
#get top 10 rearrangements by length
    filtered_names = get_largest_translocations(blocks, not_unique_scaffolds)
    output_for_circos(blocks, filtered_names, args.output)
    #output(blocks, filtered_names, args.output)
    #output(blocks, not_unique_scaffolds, args.output)
