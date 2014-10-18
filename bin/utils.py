#!/usr/bin/python
import sys
from time import gmtime, strftime
import os
import subprocess

def get_time():
        return  strftime("%Y-%m-%d-%H:%M:%S", gmtime())

def check_existence_or_raise(path):
        if not os.path.exists(path):
                raise IOError(path + ' does not exist!')
    
def create_dir_if_not_exists(path) :
        if not os.path.exists(path):
                try:
                        os.makedirs(path)
                except OSError as exception:
                        raise IOError('can not create a directory ' + path)

        else:
                if not os.path.isdir(path):
			raise IOError(path+' is not a directory!')
                    

def get_name(path) :
        base = os.path.basename(path)
        return os.path.splitext(base)[0]

def run_faSize(fasta, path_to_results):
        check_existence_or_raise(fasta)
        sizes=os.path.join(path_to_results, get_name(fasta)+'.sizes')
        params = ['faSize', '-detailed', fasta, '>', sizes]
        subprocess.call(" ".join(params), shell=True)
        return sizes
