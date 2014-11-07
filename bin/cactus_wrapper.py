#!/usr/bin/python

from ConfigParser import SafeConfigParser
import os
import subprocess
import sys
import cactus_runner

from utils import *

parser = SafeConfigParser()
parser.read('../etc/pipeline.config')

DATA_ROOT = parser.get('environment','DATA_ROOT')
VERSION = parser.get('environment','VERSION')
NAME=parser.get('environment','NAME')
PATH_TO_WORKING_DIR = os.path.join(DATA_ROOT, 'comparative', NAME, VERSION, 'cactus')

def run_cactus() :
    print 'starting wrapper for cactus', sys.argv[0], '...'
    config = os.path.join(PATH_TO_WORKING_DIR, 'cactus.config')
    check_existence_or_raise(config)
    hal = os.path.join(PATH_TO_WORKING_DIR, NAME+'_'+VERSION+'.hal')
    cactus_runner.run(config, PATH_TO_WORKING_DIR, hal)

if __name__ == '__main__' :
	run_cactus()
