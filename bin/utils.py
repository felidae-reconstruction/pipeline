#!/usr/bin/python
import sys
from time import gmtime, strftime
import os
import subprocess
import socket

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

__tmpFileCnt = 0 
def tmp_file_get(prefix=None, suffix="tmp", tmp_dir=None):
    "obtain a tmp file with a unique name"
    # FIXME should jump through security hoops, have version that returns an open name
    if tmp_dir == None:
        tmp_dir = os.getenv("TMPDIR")
    if tmp_dir == None:
        tmp_dir = "/scratch/tmp"
        if not os.path.exists(tmp_dir):
            tmp_dir = "/var/tmp"
    pre = tmp_dir
    if not pre.endswith("/"):
        pre += "/" 
    if prefix != None:
        pre += prefix + "." 
    pre += socket.gethostname() + "." + str(os.getpid())
    global __tmpFileCnt
    while True:
        path = pre + "." + str(__tmpFileCnt) + "." + suffix
        __tmpFileCnt += 1
        if not os.path.exists(path):
            return path


def atomic_tmp_file(final_path):
    "return a tmp file to use with atomic_install.  This will be in the same directory as final_path"
    final_path_dir = os.path.dirname(final_path)
    if final_path_dir == "": 
        final_path_dir = '.' 
    return tmp_file_get(prefix=os.path.basename(final_path), suffix="tmp"+os.path.splitext(final_path)[1], tmp_dir=final_path_dir)

def atomic_install(tmp_path, final_path):
    "atomic install of tmp_path as final_path"
    os.rename(tmp_path, final_path)

