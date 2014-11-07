#!/hive/groups/recon/local/bin/python

import subprocess
import utils

def run_halLiftover(hal,specie_source,genome_path,specie_target,output_prefix) :
    bed = output_prefix+'.bed'
    tmp=utils.atomic_tmp_file(bed)
    params = ['halLiftover --inMemory',hal,specie_source,genome_path,specie_target,tmp]
    params=' '.join(params)
    subprocess.call(params, shell=True)
    utils.atomic_install(tmp,bed)
    return bed

def run_sort(bed):
    sorted = bed.split('.')
    sorted.insert(1,'sorted')
    sorted = '.'.join(sorted)
    tmp=utils.atomic_tmp_file(sorted)
    params = ['bedtools sort -i', bed, '>', tmp]
    params=' '.join(params)
    subprocess.call(params, shell=True)
    utils.atomic_install(tmp,sorted)
    return sorted
    
def run_merge(sorted):
    merge = sorted.split('.')
    merge.insert(1,'merge')
    merge='.'.join(merge)
    tmp=utils.atomic_tmp_file(merge)
    params = ['bedtools merge -n -i', sorted, '>', tmp]
    params=' '.join(params) 
    subprocess.call(params, shell=True)
    utils.atomic_install(tmp,merge)
    return merge

def run(hal,specie_source,genome_path,specie_target,output_prefix) :
    print utils.get_time()
    print 'calling liftover for genome mapping annotation...'
    bed = run_halLiftover(hal,specie_source,genome_path,specie_target,output_prefix) 

    print utils.get_time()
    print 'sorting mapped entries...'
    sorted = run_sort(bed)

    print utils.get_time()
    print 'counting coverage...'
    run_merge(sorted)
    
    print utils.get_time()
    print 'done.'
