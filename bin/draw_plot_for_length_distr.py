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

def draw_distr(x,y,name):
    pp=PdfPages(name)
    plt.xlabel('length')
    plt.ylabel('number of synteny blocks')
    #bp = plt.boxplot(lengths, labels=coverages)
    bp = plt.plot(x,y)
    plt.savefig(pp, format='pdf')
    pp.close()

def save_entries(entries,name):
    with open(name, 'w') as f:
        for e in entries:
            f.write(e)

def process_lengths(values, step) :
    values.sort()
    num = 0
    max_val = step
    result_list = []
    x_range = []
    for v in values:
        if v <= max_val :
            num += 1
        else :
            result_list.append(num)
            x_range.append(max_val)
            num = 1
            max_val += step
    return x_range, result_list

        
def extract_lengths(file):
    values = []
    with open(file) as f:
        for line in f:
            val = int(line.strip())
            values.append(val)
    return values

if __name__ == '__main__' :
    if len(sys.argv) < 3:
        print 'script for calculation and drawing the length distribution for different synteny blocks values'
        print 'USAGE:', sys.argv[0], 'list_of_lengths', 'output_file_name'
    file = sys.argv[1]
    output = sys.argv[2]
    values = extract_lengths(file)
    max_val = max(values)
    x_range, values = process_lengths(values, 10000)
    print len(values), len(x_range)
    draw_distr(x_range,values,output)

