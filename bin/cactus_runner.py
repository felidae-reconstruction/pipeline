#!/usr/bin/python
import sys
from time import gmtime, strftime
import os
import subprocess

from utils import *
	
def run_cactus(config, dir, outputhal):
    check_existence_or_raise(config)
    create_dir_if_not_exists(dir)
    command = "runProgressiveCactus.sh --batchSystem parasol --bigBatchSystem singleMachine --defaultMemory 8589934593 --bigMemoryThreshold 8589934592 --bigMaxMemory 893353197568 --bigMaxCpus 25 --maxThreads 25 --parasolCommand=\'/cluster/home/jcarmstr/bin/parasol -host=ku\' --retryCount 3"
    params = [command, config, dir, outputhal]
    subprocess.call(" ".join(params), shell=True)
    return outputhal
	

if __name__ == '__main__' :
	if len(sys.argv) < 4 :
		print 'USAGE:', sys.argv[0], 'path_to_config', 'working_dir', 'path_to_hal'
	path_to_config = sys.argv[1]
	path_to_dir = sys.argv[2]
	path_to_hal = sys.argv[3]
	print get_time()
	print 'running cactus...'
	run_cactus(path_to_config, path_to_dir, path_to_hal)

