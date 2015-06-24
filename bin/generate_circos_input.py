#!/hive/groups/recon/local/bin/python

import sys
import numpy
import argparse
from collections import Counter

old_prefix2 = 'chr'
old_prefix1 = 'chr'
prefix1 = 'hum'
prefix2 = 'cat'

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
			

def sort_by_lengths(blocks):
    lengths = map(lambda x: int(x[3]), blocks)
    print max(lengths)
    print min(lengths)
    print numpy.median(lengths)
    print numpy.mean(lengths)
    z = zip(lengths, blocks)
    top = sorted(z, key = lambda x:x[0], reverse=True)
    #top = filter(lambda x: x[1][1] in must_be, top)
    sorted_blocks = map(lambda x: x[1], top)
    return sorted_blocks
	

def output_for_circos(blocks, file_name):
    with open(file_name,'w') as f:
        for e in blocks:
            id1 = e[1].split(old_prefix1)[1]
            name1 = prefix1 + id1
            id2 = e[5].split(old_prefix2)[1]
            name2 = prefix2 + id2
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
    if len(sys.argv) < 4:
        print 'USAGE:', sys.argv[0], 'blocks.txt', 'circos.txt', 'n'
        print 'n - the number of top blocks (by length)'
        exit()
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output') 
    parser.add_argument('n') 
    args = parser.parse_args()
    blocks = parse_blocks(args.input)
    #top = blocks
    top = sort_by_lengths(blocks)
    output_for_circos(top, args.output)
