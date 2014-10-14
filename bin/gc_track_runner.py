#!/usr/bin/python
import sys
from time import gmtime, strftime
import os
import subprocess

from utils import *
	
def run_faToBit(fasta, path_to_results):
	check_existence_or_raise(fasta)
	twobit = os.path.join(path_to_results, get_name(fasta)+'.2bit')
	params = ['faToTwoBit', '-noMask', fasta, twobit]
	subprocess.call(" ".join(params), shell=True)
	return twobit

def run_gcPercent(fasta, twobit, path_to_results):
	check_existence_or_raise(twobit)
	wig=os.path.join(path_to_results, 'gc5Base.'+get_name(twobit)+'.wig')	
	params = ['hgGcPercent', '-wigOut', '-doGaps', '-win=5', '-file='+wig, '-verbose=0', get_name(fasta), path_to_results]
	subprocess.call(" ".join(params), shell=True)
	return wig

def run_faSize(fasta, path_to_results):
	check_existence_or_raise(fasta)
	sizes=os.path.join(path_to_results, get_name(fasta)+'.sizes')
	params = ['faSize', '-detailed', fasta, '>', sizes]
	subprocess.call(" ".join(params), shell=True)
	return sizes

def run_wigToBigWig(fasta, wig, sizes, path_to_results):
	check_existence_or_raise(wig)
	bigWig=os.path.join(path_to_results, 'gc5Base.'+get_name(fasta)+'.bw')
	params = ['wigToBigWig', wig, sizes, bigWig]
	subprocess.call(" ".join(params), shell=True)
	return bigWig
	
def run(path_to_fasta, path_to_results) :
	print get_time()
	print 'check that folder for results exists...'
	create_dir_if_not_exists(path_to_results)

	print get_time()
	print 'running faToBit to convert fasta file to 2bit format...'
	twobit = run_faToBit(path_to_fasta, path_to_results)

	print get_time()
	print 'calculating gc content...'
	wig = run_gcPercent(path_to_fasta, twobit, path_to_results)	

	print get_time()
	print 'cacluclating sizes of fasta sequences...'
	sizes = run_faSize(path_to_fasta, path_to_results)

	print get_time()
	print 'converting wig to bigWig...'
	bigWig = run_wigToBigWig(path_to_fasta,wig, sizes, path_to_results)

	print get_time()
	print 'done.'

if __name__ == '__main__' :
	if len(sys.argv) < 3 :
		print 'USAGE:', sys.argv[0], 'path_to_fasta', 'path_to_results'
	print get_time()
	path_to_fasta = sys.argv[1]
	path_to_results = sys.argv[2]
	print 'starting ', sys.argv[0], path_to_fasta, path_to_results
	run(path_to_fasta, path_to_results)

