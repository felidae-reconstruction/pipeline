#!/hive/groups/recon/local/bin/python

from ConfigParser import SafeConfigParser
import os
import subprocess
import sys
import tempfile
import utils

HAL_PREFIX='/hive/users/ksenia/apps/hal/bin/'

def get_sequences(species, HAL):
    seqsTMP=tempfile.NamedTemporaryFile(mode='w+t')
    command = os.path.join(HAL_PREFIX,'halStats') +' --sequences ' + species + ' ' + HAL + ' > ' + seqsTMP.name
    subprocess.check_call(command, shell=True)
    seqs = []
    for line in seqsTMP:
        data = line.strip().split(',')
        data = filter(lambda x: 'scaffold' in x or 'chr' in x, data)
        seqs += data
    seqsTMP.close()
    return seqs

def get_size(scaffold, species, hal) :
    sizeTMP=tempfile.NamedTemporaryFile()
    scaffoldsTMP=tempfile.NamedTemporaryFile(mode='w+t')
    scaffoldsTMP.write(scaffold+'\n')
    scaffoldsTMP.seek(0)
    command = os.path.join(HAL_PREFIX,'halStats') +' --chromSizes ' + species + ' ' + hal + ' | fgrep -w -f ' + scaffoldsTMP.name + ' | cut -f2 > ' + sizeTMP.name
    subprocess.check_call(command, shell=True)
    scaffoldsTMP.close()
    sizes = {}
    size = int(sizeTMP.readline())
    sizeTMP.close()
    return size

def get_sizes(species, hal) :
#not tested!
    sizeTMP=tempfile.NamedTemporaryFile()
    command = os.path.join(HAL_PREFIX,'halStats') +' --chromSizes ' + species + ' ' + hal + ' > '+ sizeTMP.name
    subprocess.check_call(command, shell=True)
    sizes = []
    for line in sizeTMP.name :
        data = line.strip().split()
        sizes[data[0]] = data[1]
    return sizes

def run_joblist(joblist):
    subprocess.check_call(['para', 'make', joblist, '-ram=8g'])
    subprocess.check_call(['para', 'push'])
    subprocess.check_call(['para', 'check'])



