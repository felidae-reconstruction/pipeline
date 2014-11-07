#!/usr/bin/python
import sys
from time import gmtime, strftime
import os
import subprocess
import utils
	
def run_blat(fasta, ncrna, results):
    utils.check_existence_or_raise(fasta)
    blat_psl = os.path.join(results, utils.get_name(fasta) + '.psl')
    tmp = utils.atomic_tmp_file(blat_psl)
    params = ['blat', "-q=rna", fasta, ncrna, tmp]
    subprocess.call(" ".join(params), shell=True)
    utils.atomic_install(tmp, blat_psl)
    return blat_psl

def run_pslToBigBed(blat_psl, sizes, results):
    utils.check_existence_or_raise(blat_psl)
    blat_bed=os.path.join(results,utils.get_name(blat_psl)+'.bed')
    tmp = utils.atomic_tmp_file(blat_bed)
    params = ['pslToBed', blat_psl, tmp]
    subprocess.call(" ".join(params), shell=True)
    utils.atomic_install(tmp, blat_bed)
    sorted_bed = os.path.join(results,utils.get_name(blat_psl)+'.sorted.bed')
    tmp = utils.atomic_tmp_file(sorted_bed)
    params = ['bedSort', blat_bed, tmp]
    subprocess.call(" ".join(params), shell=True)
    utils.atomic_install(tmp, sorted_bed)
    bigBed = os.path.join(results,utils.get_name(blat_psl)+'.bigBed')
    tmp = utils.atomic_tmp_file(bigBed)
    params = ['bedToBigBed', sorted_bed, sizes, tmp]
    subprocess.call(" ".join(params), shell=True)
    utils.atomic_install(tmp, bigBed)

def  run_sorting(blat_psl, results) :
    print 'blat_psl is' ,blat_psl
    utils.check_existence_or_raise(blat_psl)
    sorted_psl = os.path.join(results,utils.get_name(blat_psl)+'.sorted.psl')
    tmp = utils.atomic_tmp_file(sorted_psl)
    params = ['sort', '-k 10,10', blat_psl, '>', tmp]
    subprocess.call(" ".join(params), shell=True)
    utils.atomic_install(tmp, sorted_psl)
    sorted_psl_only_entries = os.path.join(results,utils.get_name(blat_psl)+'.sorted.only_entries.psl') 
    tmp = utils.atomic_tmp_file(sorted_psl_only_entries)
    subprocess.call('tail -n +5 '+ sorted_psl + '| head -n -1 > ' + tmp, shell=True)
    utils.atomic_install(tmp, sorted_psl_only_entries)
    return sorted_psl_only_entries

def run_filtering(sorted_psl, results) :	
    utils.check_existence_or_raise(sorted_psl)
    stats = os.path.join(results,'filtering_stats')
    utils.create_dir_if_not_exists(stats)
    filtered_psl = os.path.join(results,utils.get_name(sorted_psl)+'.filtered.psl')    
    tmp = utils.atomic_tmp_file(filtered_psl)
    params = ['pslCDnaFilter','-localNearBest=0.1 -ignoreNs -minCover=0.6 -repsAsMatch',
			' -dropped='+os.path.join(stats,'dropped.out'), '-weirdOverlapped='+os.path.join(stats,'weird_overlapped.out'),
				'-alignStats='+os.path.join(stats,'align_stats.out'), '-statsOut='+os.path.join(stats,'overall_stats.out'),
					sorted_psl, tmp]
    subprocess.call(" ".join(params), shell=True)
    utils.atomic_install(tmp, filtered_psl)
    return filtered_psl
	

def run(fasta, ncrna, results) :
    print utils.get_time()
    print 'check that folder for results exists...'
    utils.create_dir_if_not_exists(results)
    
    print utils.get_time()
    print 'running blat...'
    blat_psl = run_blat(fasta, ncrna, results)
    
    #blat_psl = '/hive/groups/recon/projs/pipeline_data/assemblies/FelisCatus/6.2/tracks/ncrna/2014-10-18/FelisCatus.psl'
    #blat_psl = '/hive/groups/recon/projs/pipeline_data/assemblies/FelisCatus/6.2/tracks/ncrna/FelisCatus.sorted.only_entries.filtered.psl'
    print utils.get_time()
    print 'sorting blat output and adjusting file to future processing...'
    sorted_psl = run_sorting(blat_psl, results)	
    
    print utils.get_time()
    print 'filtering blat results...'
    filtered_psl = run_filtering(sorted_psl, results)
    
    print utils.get_time()
    print 'calculating sizes of fasta sequences...'
    sizes = utils.run_faSize(fasta, results)
    
    #sizes = '/hive/groups/recon/projs/pipeline_data/assemblies/FelisCatus/6.2/tracks/ncrna/2014-10-18/FelisCatus.sizes'
    print utils.get_time()
    print 'converting psl to bigBed'
    run_pslToBigBed(filtered_psl, sizes, results)
    
    print utils.get_time()
    print 'done.'
