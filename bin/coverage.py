#!/hive/groups/recon/local/bin/python

import bisect
import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import threading
from numpy import array
import utils

def draw_distr(lengths,coverages,name):
    pp=PdfPages(name)
    bp = plt.boxplot(lengths, labels=coverages)
    plt.savefig(pp, format='pdf')
    pp.close()

def extract_coverage(file):
    print utils.get_time()
    print 'loading the data from file...'
    covs=[]
    lengths=[]
    with open(file,'r') as f:
        data = f.readline()
        while data:
            entries = data.split()
            if len(entries) < 4:
                continue
            start = long(entries[1])
            end = long(entries[2])
            length = end - start
            coverage = int(entries[3])
            covs.append(coverage)
            lengths.append(length)
            data = f.readline()
    return covs, lengths

def count_lengths_distribution_for_coverage(c,z):
    print utils.get_time()
    print 'calculating for coverage',c
    filtered_lengths = [j for _,j in filter(lambda x : x[0] == c,z)]
    print 'data size is',len(filtered_lengths)
    return filtered_lengths

def process_coverage(covs,lengths):
    print utils.get_time()
    print 'processing the data...'
    z = zip(covs,lengths)
    unique_covs = sorted(list(set(covs)))
    if 1 in unique_covs:
        unique_covs.remove(1)
    filtered_lengths=[]
    for c in unique_covs:
        if c == 27 :
            break
        filtered_lengths.append(count_lengths_distribution_for_coverage(c,z))
    draw_distr(filtered_lengths[:24],unique_covs[:24],'2-25.pdf')

         

if __name__ == '__main__' :
    if len(sys.argv) < 2:
        print 'script for calculation and drawing the length distribution for different coverage values'
        print 'USAGE:', sys.argv[0], 'file in bed format having four columns - the last one is the coverage values'
    file = sys.argv[1]
    covs,lengths = extract_coverage(file)
    print utils.get_time()
    process_coverage(covs,lengths)
