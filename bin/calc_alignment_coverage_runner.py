#!/hive/groups/recon/local/bin/python

import subprocess
from utils import *

def run_halLiftover(hal,specie_source,genome_path,specie_target,output_prefix) :
    bed = output_prefix+'.bed'
    params = ['halLiftover --inMemory',hal,specie_source,genome_path,specie_target,bed]
    params=' '.join(params)
    subprocess.call(params, shell=True)
    return bed

def run_sort(bed):
    sorted = bed+'.sorted'
    params = ['bedtools sort -i', bed, '>', sorted]
    params=' '.join(params)
    subprocess.call(params, shell=True)
    return sorted
    
def run_merge(sorted):
    merge = sorted+'.merge'
    params = ['bedtools merge -n -i', sorted, '>', merge]
    params=' '.join(params) 
    subprocess.call(params, shell=True)
    return merge

def run(hal,specie_source,genome_path,specie_target,output_prefix) :
    print get_time()
    print 'calling liftover for genome mapping annotation...'
    bed = run_halLiftover(hal,specie_source,genome_path,specie_target,output_prefix) 

    print get_time()
    print 'sorting mapped entries...'
    sorted = run_sort(bed)

    print get_time()
    print 'counting coverage...'
    run_merge(sorted)
    
    print get_time()
    print 'done.'
