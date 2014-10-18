#!/usr/bin/python
import sys
from time import gmtime, strftime
import os
import subprocess

from utils import *
	
def run_blat(fasta, ncrna, results):
	check_existence_or_raise(fasta)
	blat_psl = os.path.join(results, get_name(fasta) + '.psl')
	params = ['blat', "-q=rna", fasta, ncrna, blat_psl]
	subprocess.call(" ".join(params), shell=True)
	return blat_psl

def run_pslToBigBed(blat_psl, sizes, results):
	check_existence_or_raise(blat_psl)
	blat_bed=os.path.join(results,get_name(blat_psl)+'.bed')	
	params = ['pslToBed', blat_psl,  blat_bed]
	subprocess.call(" ".join(params), shell=True)
	sorted_bed = os.path.join(results,get_name(blat_psl)+'.sorted.bed')
	params = ['bedSort', blat_bed, sorted_bed]
	subprocess.call(" ".join(params), shell=True)
	bigBed = os.path.join(results,get_name(blat_psl)+'.bigBed')
	params = ['bedToBigBed', sorted_bed, sizes, bigBed]
	subprocess.call(" ".join(params), shell=True)

def  run_sorting(blat_psl, results) :
	print 'blat_psl is' ,blat_psl
	check_existence_or_raise(blat_psl)
	sorted_psl = os.path.join(results,get_name(blat_psl)+'.sorted.psl') 
	params = ['sort', '-k 10,10', blat_psl, '>', sorted_psl]
	subprocess.call(" ".join(params), shell=True)
	sorted_psl_only_entries = os.path.join(results,get_name(blat_psl)+'.sorted.only_entries.psl') 
	subprocess.call('tail -n +5 '+ sorted_psl + '| head -n -1 > ' + sorted_psl_only_entries, shell=True)
	return sorted_psl_only_entries

def run_filtering(sorted_psl, results) :	
	check_existence_or_raise(sorted_psl)
	stats = os.path.join(results,'filtering_stats')
	create_dir_if_not_exists(stats)
	filtered_psl = os.path.join(results,get_name(sorted_psl)+'.filtered.psl')    
	params = ['pslCDnaFilter','-localNearBest=0.1 -ignoreNs -minCover=0.6 -repsAsMatch',
			' -dropped='+os.path.join(stats,'dropped.out'), '-weirdOverlapped='+os.path.join(stats,'weird_overlapped.out'),
				'-alignStats='+os.path.join(stats,'align_stats.out'), '-statsOut='+os.path.join(stats,'overall_stats.out'),
					sorted_psl, filtered_psl]
	subprocess.call(" ".join(params), shell=True)
	return filtered_psl
	

def run(fasta, ncrna, results) :
	print get_time()
	print 'check that folder for results exists...'
	create_dir_if_not_exists(results)

	print get_time()
	print 'running blat...'
	blat_psl = run_blat(fasta, ncrna, results)

	#blat_psl = '/hive/groups/recon/projs/pipeline_data/assemblies/FelisCatus/6.2/tracks/ncrna/2014-10-18/FelisCatus.psl'
	print get_time()
	print 'sorting blat output and adjusting file to future processing...'
	sorted_psl = run_sorting(blat_psl, results)	

	print get_time()
	print 'filtering blat results...'
	filtered_psl = run_filtering(sorted_psl, results)

	print get_time()
	print 'calculating sizes of fasta sequences...'
	sizes = run_faSize(fasta, results)

	#sizes = '/hive/groups/recon/projs/pipeline_data/assemblies/FelisCatus/6.2/tracks/ncrna/2014-10-18/FelisCatus.sizes'
	print get_time()
	print 'converting psl to bigBed'
	run_pslToBigBed(filtered_psl, sizes, results)

	print get_time()
	print 'done.'

if __name__ == '__main__' :
	if len(sys.argv) < 4 :
		print 'USAGE:', sys.argv[0], 'path_to_fasta', 'path_to_ncrna.fasta', 'path_to_results'
	print get_time()
	fasta = sys.argv[1]
	ncrna = sys.argv[2]
	results = sys.argv[3]
	print 'starting ', sys.argv[0], fasta, ncrna, results
	run(fasta, ncrna, results)

