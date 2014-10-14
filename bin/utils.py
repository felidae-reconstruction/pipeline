#!/usr/bin/python
import sys
from time import gmtime, strftime
import os


def get_time():
        return  strftime("%Y-%m-%d %H:%M:%S", gmtime())

def check_existence_or_raise(path):
        if not os.path.exists(path):
                raise Error(path + ' does not exist!')
    
def create_dir_if_not_exists(path) :
        if not os.path.exists(path):
                try:
                        os.makedirs(path)
                except OSError as exception:
                        raise Error('can not create a directory ' + path)

        else:
                if not os.path.isdir(path):
			raise Error(path+' is not a directory!')
                    

def get_name(path) :
        base = os.path.basename(path)
        return os.path.splitext(base)[0]

def get_time() :
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

