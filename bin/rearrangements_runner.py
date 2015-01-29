#!/hive/groups/recon/local/bin/python
import sys
from time import gmtime, strftime
import os
import subprocess
import utils

def create_bigBed(grimm_synt_output, sizes_folder, species_file):
    blocks = os.path.join(grimm_synt_output,'blocks.txt')
    bed = os.path.join(grimm_synt_output,'bed')
    utils.create_dir_if_not_exists(bed)
    params = ['./blocks_to_bed.py', blocks, bed]
    subprocess.call(" ".join(params), shell=True)
    with open(species_file) as species:
        for line in species :
            line = line.strip().split(' ')
            if len(line) < 2:
                print 'species file format: genome_id genome_name'
                print 'no bigBeds generated'
                return
            params = ['sort -k1,1 -k2,2n', os.path.join(bed,line[0]+'.bed'), '>', os.path.join(bed,line[0]+'.sorted.bed')]
            subprocess.call(" ".join(params), shell=True)
            params = ['bedToBigBed -type=bed6', os.path.join(bed,line[0]+'.sorted.bed'), os.path.join(sizes_folder,line[1]+'.sizes'), os.path.join(bed,line[1]+'.bb')]
            subprocess.call(" ".join(params), shell=True)
    print 'path to bigBed folder is',bed 


	
def run(dir, maf, sizes_folder, species_file):
    grimm_synt_input_file = os.path.join(dir, utils.get_name(maf)+'.grimm_synt')
    print utils.get_time()
    print 'converting maf to input for grimm...'
    params = ['./generate_input_grimm_synt.py', maf, sizes_folder, grimm_synt_input_file, species_file]
    subprocess.call(" ".join(params), shell=True)
    print utils.get_time()
    print 'generating anchors for grimm_synt...'
    anchors_folder = os.path.join(dir,'grimm_synt_anchors')
    utils.create_dir_if_not_exists(anchors_folder)
    params = ['grimm_synt', '-A -f', grimm_synt_input_file, '-d', anchors_folder]
    subprocess.call(" ".join(params), shell=True)
    print utils.get_time()
    print 'running grimm_synt...'
    grimm_synt_output = os.path.join(dir,'grimm_synt_output')
    utils.create_dir_if_not_exists(grimm_synt_output)
    params = ['grimm_synt','-f', os.path.join(anchors_folder, 'unique_coords.txt'),'-d',grimm_synt_output, '-m 1000 -g 1000 -c']
    #params = ['grimm_synt','-f', os.path.join(anchors_folder, 'unique_coords.txt'),'-d',grimm_synt_output,'-m 300000 -g 300000 -c']
    subprocess.call(" ".join(params), shell=True)
    print 'synteny blocks are at',os.path.join(grimm_synt_output,'blocks.txt')
    print utils.get_time()
    print 'creating bigBed files...'
    create_bigBed(grimm_synt_output, sizes_folder, species_file)
    print utils.get_time()
    '''print 'running grimm...'
    params = ['grimm', '-f', os.path.join(grimm_synt_output,'mgr_macro.txt'), '-o', os.path.join(dir,'grimm.output')]
    subprocess.call(" ".join(params), shell=True)
    print 'grimm output is saved to', os.path.join(dir,'grimm.output')
    print utils.get_time()
    '''
    print 'done.'
    
	
