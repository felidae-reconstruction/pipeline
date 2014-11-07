#!/usr/bin/python
import sys
from time import gmtime, strftime
import os
import subprocess
import utils
	
def run_faToBit(fasta, path_to_results):
    utils.check_existence_or_raise(fasta)
    twobit = os.path.join(path_to_results, utils.get_name(fasta)+'.2bit')
    tmp = utils.atomic_tmp_file(twobit)
    params = ['faToTwoBit', '-noMask', fasta, tmp]
    subprocess.call(" ".join(params), shell=True)
    utils.atomic_install(tmp,twobit)
    return twobit

def run_gcPercent(fasta, twobit, path_to_results):
    utils.check_existence_or_raise(twobit)
    wig=os.path.join(path_to_results, 'gc5Base.'+utils.get_name(twobit)+'.wig')	
    tmp = utils.atomic_tmp_file(wig)
    params = ['hgGcPercent', '-wigOut', '-doGaps', '-win=5', '-file='+tmp, '-verbose=0', utils.get_name(fasta), path_to_results]
    subprocess.call(" ".join(params), shell=True)
    utils.atomic_install(tmp,wig)
    return wig

def run_wigToBigWig(fasta, wig, sizes, path_to_results):
    utils.check_existence_or_raise(wig)
    bigWig=os.path.join(path_to_results, utils.get_name(fasta)+'.gc5Base'+'.bw')
    tmp = utils.atomic_tmp_file(bigWig)
    params = ['wigToBigWig', wig, sizes, tmp]
    subprocess.call(" ".join(params), shell=True)
    utils.atomic_install(tmp,bigWig)
    return bigWig
	
def run(path_to_fasta, path_to_results) :
	print utils.get_time()
	print 'check that folder for results exists...'
	utils.create_dir_if_not_exists(path_to_results)

	print utils.get_time()
	print 'running faToBit to convert fasta file to 2bit format...'
	twobit = run_faToBit(path_to_fasta, path_to_results)

	print utils.get_time()
	print 'calculating gc content...'
	wig = run_gcPercent(path_to_fasta, twobit, path_to_results)	

	print utils.get_time()
	print 'cacluclating sizes of fasta sequences...'
	sizes = utils.run_faSize(path_to_fasta, path_to_results)

	print utils.get_time()
	print 'converting wig to bigWig...'
	bigWig = run_wigToBigWig(path_to_fasta,wig, sizes, path_to_results)

	print utils.get_time()
	print 'done.'

