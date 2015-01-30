#!/hive/groups/recon/local/bin/python

from ConfigParser import SafeConfigParser
import os
import subprocess
import sys
import tempfile
import utils
from chaining_utils import *

parser = SafeConfigParser()
parser.read('../etc/chaining.config')

DATA_ROOT = parser.get('environment','DATA_ROOT')
VERSION = parser.get('environment','VERSION')
HAL = parser.get('environment','HAL')
NAME = parser.get('environment','NAME')
QUERY = parser.get('environment','QUERY')
TARGET = parser.get('environment','TARGET')
PATH_TO_WORKING_DIR = os.path.join(DATA_ROOT, 'comparative', NAME, VERSION)


def create_bed(bed_split_dir, id, scaffolds):
    #bedTMP=tempfile.NamedTemporaryFile()
    bedname = os.path.join(bed_split_dir, str(id)+'.bed')
    sizes = get_sizes(scaffolds, QUERY, HAL)
    with open(bedname, 'w') as f:
        for s in scaffolds:
            f.write(s + ' 0 ' + sizes[s]+'\n')
    #    bedTMP.write(s + ' 0 ' + sizes[s]+'\n')
    #bedTMP.seek(0)
    #return bedTMP.name
    return bedname

def split_beds_by_query() :
    query_sequences = get_sequences(QUERY, HAL)
    bed_split_dir = os.path.join(PATH_TO_WORKING_DIR,'queryBedSplit')
    utils.create_dir_if_not_exists(bed_split_dir)
    chunk_size = len(query_sequences) / 100
    start = 0
    end = chunk_size
    bed_names = []
    for i in range(100):
        subset = query_sequences[start:end]
        start += chunk_size
        end += chunk_size
        bed_names.append(create_bed(bed_split_dir, i, subset))
    return bed_names

def create_joblist_for_halliftover(bed_names, halliftover_output_dir) :
    joblist_name = os.path.join(PATH_TO_WORKING_DIR,'joblist_halLiftover')
    with open(joblist_name,'w') as f:
        for bed in bed_names:
            command = 'chain_scripts/run_halliftover.sh ' + HAL + ' ' + QUERY + ' ' + bed + ' ' + TARGET + ' ' +\
                        os.path.join(halliftover_output_dir,utils.get_name(bed)+'.psl')
            f.write(command+'\n')
    return joblist_name


#def split_psl_by_target(overall_psl, target_chrs, output_dir) :
#    for ch in target_chrs:
#        subprocess.call('tawk -v chrom='+ch+' \'{if ($14 == chrom) print $0}\'' + overall_psl + ' >> ' +\
#                        os.path.join(output_dir,ch+'.'+TARGET+'.'+QUERY+'.psl', shell=True))

def run() :
    liftover_output_dir = os.path.join(PATH_TO_WORKING_DIR,'halLiftover_output')
    utils.create_dir_if_not_exists(liftover_output_dir)
    bed_names = split_beds_by_query()
    joblist = create_joblist_for_halliftover(bed_names, liftover_output_dir)
    run_joblist(joblist)

    overall_halliftover_result = os.path.join(liftover_output_dir,'/'+QUERY+'.'+TARGET+'.psl')
    print 'liftover output dir is', liftover_output_dir
    #subprocess.call('cat ' +liftover_output_dir+ '/* > '+overall_halliftover_result)
    #split_target_output_dir = os.path.join(PATH_TO_WORKING_DIR,'pslSplitHalLift')
    #subprocess.call('pslSplitOnTarget ' + overall_halliftover_result + ' ' + split_target_output_dir)
    

if __name__ == '__main__':
    utils.create_dir_if_not_exists(PATH_TO_WORKING_DIR)
    run()
