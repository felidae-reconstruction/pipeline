#!/hive/groups/recon/local/bin/python

#reads mgr_micro.txt file and calculates 
#density of anchors comprising synteny blocks
#i.e. length(sum of anchors lengths) / length(block_length)

import sys
import numpy
import argparse

#genome_id is one-based
def parse_mgr_micro(path, genome_id) :
    with open(path) as f:
        anchor_lengths = []
        block_lengths = []
        skip_mgr = False
        for line in f:
            line = line.strip()
            data = line.split()
            if 'end_mgr' in line:
                skip_mgr = False
                continue
            if skip_mgr :
                continue
            if 'begin_block' in line:
                anchor_lengths.append(0.0)
                base = 2 + (genome_id - 1) * 4
                block_lengths.append(int(data[base + 3]))
                continue
            if 'begin_mgr' in line:
                skip_mgr = True
                continue
            if '#' in line:
                continue
            base = (genome_id - 1) * 4
            length = int(data[base + 3])
            anchor_lengths[-1] += length
    return anchor_lengths, block_lengths



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('genome_id')
    args = parser.parse_args()
    anchor_lengths, block_lengths = parse_mgr_micro(args.path, int(args.genome_id))
    rates = [a/b for a,b in zip(anchor_lengths, block_lengths)]
    print 'min density', min(rates)
    print 'max density', max(rates)
    print 'median density', numpy.median(rates)
    #for i in range(len(rates)):
    #    print i+1, rates[i]
