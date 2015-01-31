#!/hive/groups/recon/local/bin/python

import os
import subprocess
import sys
import tempfile
import utils
from chaining_utils import *

def create_bed(hal, query, chromosome):
    bedTMP=tempfile.NamedTemporaryFile(mode='w+t',delete=False)
    size = get_size(chromosome, query, hal)
    bedTMP.write(chromosome + ' 0 ' + str(size)+'\n')
    bedTMP.flush()
    bedTMP.seek(0)
    return bedTMP


def create_joblist_for_halliftover(hal, query, target, bed, psl) :
    jobList=tempfile.NamedTemporaryFile(mode='w+t',delete=False)
    print bed
    command = 'chain_scripts/run_halliftover.sh ' + hal + ' ' + query + ' ' + bed + ' ' + target + ' ' + psl
    #command = 'chain_scripts/run_halliftover.sh ' + hal + ' ' + query + ' ' + 'scaffold.bed' + ' ' + target + ' ' + psl
    print command
    jobList.write(command+'\n')
    jobList.flush()
    jobList.seek(0)
    return jobList


def run(hal, query, target, chromosome, psl) :
    bed = create_bed(hal, query, chromosome)
    joblist = create_joblist_for_halliftover(hal, query, target, bed.name, psl)
    print joblist.name
    run_joblist(joblist.name)

if __name__ == '__main__':
    hal = sys.argv[1]
    query = sys.argv[2]
    target = sys.argv[3]
    chromosome = sys.argv[4]
    psl = sys.argv[5]
    run(hal, query, target, chromosome, psl)
