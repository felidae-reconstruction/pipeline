#!/usr/bin/python
import sys
from time import gmtime, strftime
import os
import subprocess
import utils
	
def run(config, dir, outputhal):
    utils.check_existence_or_raise(config)
    utils.create_dir_if_not_exists(dir)
    command = 'runProgressiveCactus.sh --batchSystem parasol --bigBatchSystem singleMachine'\
    ' --defaultMemory 8589934593 --bigMemoryThreshold 8589934592 --bigMaxMemory 893353197568'\
    ' --bigMaxCpus 25 --maxThreads 25 --parasolCommand=\'/cluster/home/jcarmstr/bin/parasol -host=ku\''\
    ' --retryCount 3'
    print command
    params = [command, config, dir, outputhal]
    subprocess.call(" ".join(params), shell=True)
    return outputhal
	
