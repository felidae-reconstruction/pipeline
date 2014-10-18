#!/usr/bin/python

from ConfigParser import SafeConfigParser
import os
import subprocess
import sys

from utils import *

parser = SafeConfigParser()
parser.read('../etc/pipeline.config')

DATA_ROOT = parser.get('environment','DATA_ROOT')
ORGANISM = parser.get('environment','ORGANISM')
VERSION = parser.get('environment','VERSION')
NAME=parser.get('environment','NAME')
PATH_TO_FASTA_DIR = os.path.join(DATA_ROOT, 'assemblies', ORGANISM, VERSION)
PATH_TO_OUTPUT = os.path.join(PATH_TO_FASTA_DIR, 'tracks', NAME, get_time())

def get_fasta_files_from_dir(path) :
	files = os.listdir(path)
	return filter(lambda x : os.path.splitext(x)[1] in ['.fa','.fasta'], files)
	


def run_gc_track() :
	if NAME != gc :
		print 'config file is not for gc track'
		print 'done.'
	print 'starting wrapper for gc track from', sys.argv[0], '...'
	fasta = os.path.join(PATH_TO_FASTA_DIR, ORGANISM+'.fa')
	params = ['./gc_track_runner.py', fasta, PATH_TO_OUTPUT] 
	subprocess.call(" ".join(params), shell=True)

if __name__ == '__main__' :
	run_gc_track()
