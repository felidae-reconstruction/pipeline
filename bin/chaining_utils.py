#!/hive/groups/recon/local/bin/python

from ConfigParser import SafeConfigParser
import os
import subprocess
import sys
import tempfile
import utils

def get_sequences(species, HAL):
    seqsTMP=tempfile.NamedTemporaryFile()
    command = 'halStats --sequences ' + species + ' ' + HAL + ' > ' + seqsTMP.name
    subprocess.call(command, shell=True)
    seqs = []
    for line in seqsTMP:
        data = line.strip().split(',')
        seqs += data
    seqsTMP.close()
    return seqs

def get_sizes(scaffolds, species, HAL):
    sizeTMP=tempfile.NamedTemporaryFile()
    scaffoldsTMP=tempfile.NamedTemporaryFile(mode='w+t')
    for s in scaffolds:
        scaffoldsTMP.write(s+'\n')
    scaffoldsTMP.seek(0)
    command = 'halStats --chromSizes ' + species + ' ' + HAL + ' | fgrep -w -f ' + scaffoldsTMP.name + ' > ' + sizeTMP.name
    subprocess.call(command, shell=True)
    scaffoldsTMP.close()
    sizes = {}
    for line in sizeTMP:
        data = line.strip().split()
        sizes[data[0]] = data[1]
    sizeTMP.close()
    return sizes

def run_joblist(joblist):
    subprocess.call('para create '+joblist+' -ram=8g', shell=True)
    subprocess.call('para try ; para check ;', shell=True)
    subprocess.call('para push; para check;', shell=True)


