#!/usr/bin/python

from ConfigParser import SafeConfigParser
import os
import subprocess
import sys

parser = SafeConfigParser()
parser.read('../pipeline.config')

DATA_ROOT = parser.get('environment','DATA_ROOT')
ORGANISM = parser.get('environment','ORGANISM')
VERSION = parser.get('environment','VERSION')
NAME=parser.get('environment','NAME')
PATH_TO_FASTA_DIR = os.path.join(DATA_ROOT, 'assemblies', ORGANISM, VERSION)
PATH_TO_OUTPUT = os.path.join(PATH_TO_FASTA_DIR, 'tracks', NAME)

def get_fasta_files_from_dir(path) :
	files = os.listdir(path)
	return filter(lambda x : os.path.splitext(x)[1] in ['.fa','.fasta'], files)
	


def run_gc_track() :
	print 'starting wrapper for gc track from', sys.argv[0], '...'
	if not os.path.exists(PATH_TO_FASTA_DIR) :
		print PATH_TO_FASTA_DIR, 'does not exist'
	fasta_files = get_fasta_files_from_dir(PATH_TO_FASTA_DIR)
	for fasta in fasta_files:
		params = ['./gc_track_runner.py', os.path.join(PATH_TO_FASTA_DIR, fasta), PATH_TO_OUTPUT] 
		subprocess.call(" ".join(params), shell=True)

if __name__ == '__main__' :
	run_gc_track()
