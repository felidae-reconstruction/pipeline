#!/hive/groups/recon/local/bin/python

from ConfigParser import SafeConfigParser
import os
import subprocess
import sys
import utils

parser = SafeConfigParser()
parser.read('../etc/chaining.config')

DATA_ROOT = parser.get('environment','DATA_ROOT')
VERSION = parser.get('environment','VERSION')
HAL = parser.get('environment','HAL')
NAME = parser.get('environment','NAME')
SIZES_FOLDER=parser.get('environment','SIZES_FOLDER')
QUERY = parser.get('environment','QUERY')
TARGET = parser.get('environment','TARGET')
PATH_TO_WORKING_DIR = os.path.join(DATA_ROOT, 'comparative', NAME, VERSION)

def parse_sizes():
    query_sizes = os.path.join(SIZES_FOLDER, QUERY + '.sizes')
    sizes = []
    with open(query_sizes) as f:
        for line in f:
            data = line.strip().split()
            sizes.append((data[0],data[1]))
    return sizes

def create_bed(bed_split_dir, id, scaffolds):
    bed_path = os.path.join(bed_split_dir,str(id)+'.bed')
    with open(bed_path,'w') as f:
        for e in scaffolds:
            f.write(e[0] + ' 0 ' + e[1]+'\n')
    return bed_path

def split_beds() :
    query_sizes = parse_sizes()
    bed_split_dir = os.path.join(PATH_TO_WORKING_DIR,'queryBedSplit')
    utils.create_dir_if_not_exists(bed_split_dir)
    chunk_size = len(query_sizes) / 100
    start = 0
    end = chunk_size
    bed_names = []
    for i in range(100):
        subset = query_sizes[start:end]
        start += chunk_size
        end += chunk_size
        bed_names.append(create_bed(bed_split_dir, i, subset))
    return bed_names

def create_joblist_for_halliftover(bed_names, halliftover_output_dir) :
    joblist_name = os.path.join(PATH_TO_WORKING_DIR,'joblist_halLiftover')
    with open(joblist_name,'w') as f:
        for bed in bed_names:
            command = '../chain_scripts/run_halliftover.sh ' + HAL + ' ' + QUERY + ' ' + bed + ' ' + TARGET + ' ' +\
                        os.path.join(halliftover_output_dir,utils.get_name(bed)+'.psl')
            f.write(command+'\n')
    return joblist_name

def run_joblist(joblist):
    subprocess.call('para create '+joblist+' -ram=8g', shell=True)
    subprocess.call('para try ; para check ;', shell=True)
    subprocess.call('para push; para check;', shell=True)

def split_psl_by_target(overall_psl, target_chrs, output_dir) :
    for ch in target_chrs:
        subprocess.call('tawk -v chrom='+ch+' \'{if ($14 == chrom) print $0}\'' + overall_psl + ' >> ' +\
                        os.path.join(output_dir,ch+'.'+TARGET+'.'+QUERY+'.psl', shell=True))

def run() :
    liftover_output_dir = os.path.join(PATH_TO_WORKING_DIR,'halLiftover_output')
    utils.create_dir_if_not_exists(liftover_output_dir)
    bed_names = split_beds()
    joblist = create_joblist_for_halliftover(bed_names, liftover_output_dir)
    pwd = os.getcwd()
    run_joblist(joblist)

    overall_halliftover_result = os.path.join(liftover_output_dir,'/'+QUERY+'.'+TARGET+'.psl')
    print 'liftover output dir is', liftover_output_dir
    #subprocess.call('cat ' +liftover_output_dir+ '/* > '+overall_halliftover_result)
    #split_target_output_dir = os.path.join(PATH_TO_WORKING_DIR,'pslSplitHalLift')
    #subprocess.call('pslSplitOnTarget ' + overall_halliftover_result + ' ' + split_target_output_dir)
    

if __name__ == '__main__':
    utils.create_dir_if_not_exists(PATH_TO_WORKING_DIR)
    run()
