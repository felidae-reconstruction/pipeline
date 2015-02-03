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
        data = filter(lambda x: 'scaffold' in x, data)
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

'''
def get_sizes(scaffolds, species, HAL):
    sizeTMP=tempfile.NamedTemporaryFile()
    scaffoldsTMP=tempfile.NamedTemporaryFile(mode='w+t')
    for s in scaffolds:
        scaffoldsTMP.write(s+'\n')
    scaffoldsTMP.seek(0)
    command = os.path.join(HAL_PREFIX,'halStats') +' --chromSizes ' + species + ' ' + HAL + ' | fgrep -w -f ' + scaffoldsTMP.name + ' > ' + sizeTMP.name
    subprocess.check_call(command, shell=True)
    scaffoldsTMP.close()
    sizes = {}
    for line in sizeTMP:
        data = line.strip().split()
        sizes[data[0]] = data[1]
    sizeTMP.close()
    return sizes
'''

def run_joblist(joblist):
    subprocess.check_call('para create '+joblist+' -ram=16g', shell=True)
    subprocess.check_call('para try ; para check;', shell=True)
    subprocess.check_call('para push; para check;', shell=True)


