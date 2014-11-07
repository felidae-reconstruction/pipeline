#!/usr/bin/python

from ConfigParser import SafeConfigParser
import os
import subprocess
import sys
import ncrna_track_runner

from utils import *

parser = SafeConfigParser()
parser.read('../etc/pipeline.config')

DATA_ROOT = parser.get('environment','DATA_ROOT')
ORGANISM = parser.get('environment','ORGANISM')
VERSION = parser.get('environment','VERSION')
NAME=parser.get('environment','NAME')
SCRIPT_PARAMS=parser.get('environment','SCRIPT_PARAMS')
PATH_TO_GENOME_DIR = os.path.join(DATA_ROOT, 'assemblies', ORGANISM, VERSION, 'genome')
PATH_TO_TRACK_DIR = os.path.join(DATA_ROOT, 'assemblies', ORGANISM, VERSION, 'tracks', NAME)
PATH_TO_OUTPUT = os.path.join(PATH_TO_TRACK_DIR, get_time())


def run_ncrna_track() :
    if (NAME != 'ncrna') :
        print 'script config is not for ncrna'
        print 'done.'
    print 'starting wrapper for ncrna track from', sys.argv[0], '...'
    ncrna = os.path.join(PATH_TO_TRACK_DIR, SCRIPT_PARAMS)
    genome_file = os.path.join(PATH_TO_GENOME_DIR, ORGANISM + '.fa')
    check_existence_or_raise(genome_file)
    check_existence_or_raise(ncrna)
    ncrna_track_runner.run(genome_file, ncrna, PATH_TO_OUTPUT)

if __name__ == '__main__' :
	run_ncrna_track()
