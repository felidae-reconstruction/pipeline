#!/usr/bin/python

from ConfigParser import SafeConfigParser
import os
import subprocess
import sys
import calc_alignment_coverage_runner
from utils import *

parser = SafeConfigParser()
parser.read('../etc/pipeline.config')

DATA_ROOT = parser.get('environment','DATA_ROOT')
SPECIE_SOURCE = parser.get('environment','SPECIE_SOURCE')
SPECIE_TARGET = parser.get('environment','SPECIE_TARGET')
NAME=parser.get('environment','NAME')
PATH_TO_HAL = parser.get('environment','PATH_TO_HAL') 
PATH_TO_FASTA = parser.get('environment','PATH_TO_FASTA')  
PATH_TO_BED = parser.get('environment','PATH_TO_BED')  
PATH_TO_OUTPUT = parser.get('environment','PATH_TO_OUTPUT')  
PATH_TO_OUTPUT = os.path.join(PATH_TO_OUTPUT, get_time())

def get_fasta_files_from_dir(path) :
	files = os.listdir(path)
	return filter(lambda x : os.path.splitext(x)[1] in ['.fa','.fasta'], files)
	


def run_coverage_calc():
    if NAME != 'coverage' :
        print 'config file is not for coverage'
        print 'done.'
    print 'starting wrapper for alignment coverage from', sys.argv[0], '...'
    create_dir_if_not_exists(PATH_TO_OUTPUT)
    prefix = os.path.join(PATH_TO_OUTPUT, 'coverage.'+SPECIE_SOURCE+'.'+SPECIE_TARGET)
    calc_alignment_coverage_runner.run(PATH_TO_HAL,SPECIE_SOURCE,PATH_TO_BED,PATH_TO_FASTA,SPECIE_TARGET,prefix) 

if __name__ == '__main__' :
	run_coverage_calc()
