#!/hive/groups/recon/local/bin/python
'''
script for calculation and drawing the length distribution for different synteny blocks values
'''

import bisect
import sys
import argparse
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import threading
import numpy
import utils

def draw_distr(x,y,name):
    pp=PdfPages(name)
    plt.xlabel('Length')
    plt.ylabel('Number of synteny blocks')
    ##plt.tick_params(axis='both', which='major', labelsize=10)
    plt.ticklabel_format(style='sci',scilimits=(0,0))
    #major_formatter = plt.FormatStrFormatter('%2.1f')
    #plt.gca().xaxis.set_major_formatter(major_formatter)
    plt.tick_params(axis='both', which='minor', labelsize=10)
    ##bp = plt.plot(x,y)
    plt.bar(x, y, align='center', width=100000, color='green')
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
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('output')
    args = parser.parse_args()
    values = extract_lengths(args.file)
    print 'min:', min(values), 'max:', max(values), 'median:', numpy.median(values)
    max_val = max(values)
    x_range, values = process_lengths(values, 200000)
    #print len(values), len(x_range)
    draw_distr(x_range,values,args.output)

