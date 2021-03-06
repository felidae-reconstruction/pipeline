#!/hive/groups/recon/local/bin/python

import sys
import os
import utils

'''
get file in format
chromosomes strand name=actual_name
'''
def parse_genes(file):
    print file
    if (file.split('.')[-1] != 'gff'):
        'the', file, 'is not a .gff file!'
        exit()
    chromosomes = {}
    with open(file,'r') as f:
        for line in f:
            data = line.split()
            chromosome = data[0] 
            strand = data[1]
            name = (data[2].split(';')[0]).split('=')
            if (name[0] == 'Parent') :
                continue
            name = name[1]
            if chromosome in chromosomes :
                l = chromosomes.pop(chromosome)
                l.append((name,strand))
                chromosomes[chromosome]=l
            else :
                chromosomes[chromosome]=[(name,strand)]
    return chromosomes

'''
Parse homology file in format:
genomeA genomeB
geneA1 geneB3 #1
geneA2,geneA3 geneB4 #2
geneA4 geneB1,geneB2 #3
...

in case of #2 adds to the cross_species_homology the pairs (geneA2, geneB4), (geneA3, geneB4) 
in case of #3 adds to inter_species_homology of genomeA (geneB2, geneB1)
'''

def get_first_element(l) :
    return l[0]

def parse_homology(homology_file):
    homology=dict()
    with open(homology_file,'r') as f:
        f.readline()
        for line in f:
            data = line.split()
            left = data[0].split(',')
            right = data[1].split(',')
            if len(left) > 1 or len(right) > 1 or right[0] == '*' or left[0] == '*' :
                continue
            homology[left[0]] = right[0]
    return homology

'''
all_genes is the dictionary of {chromosome=[(name,strand)]} for the genome genome_name
homology is the homology relationship {gene1=gene2}. according to this mapping the genes in the genome genome_name are renamed
coding_table is the ordered list [gene]. indexes of the genes will be representations of genes for the grimm input
'''
def output_genes(genome_name, all_genes, homology, file) :
    num = 0
    coding_table = []
    with open(file, 'w') as f:
        new_names = homology.values()
        f.write('>'+genome_name+'\n')
        for chromosome in all_genes :
            end_of_chromosome = ''
            #f.write('>'+chromosome+'\n')
            genes = all_genes[chromosome]
            for pair in genes:
                name = pair[0]
                sign = ''
                if name in new_names :
                        if pair[1] == '-':
                            sign = '-'
                        num += 1
                        end_of_chromosome = '$\n'
                        coding_table.append(name)
                        code =len( coding_table)
                        f.write(sign+str(code)+' ')
            f.write(end_of_chromosome)
    print 'num', num
    return coding_table
           
def output_genes_and_rename(genome_name, all_genes, homology, coding_table, file):
    num = 0
    with open(file, 'a') as f:
        old_names = homology.keys()
        f.write('>'+genome_name+'\n')
        for chromosome in all_genes :
            end_of_chromosome = ''
            #f.write('>'+chromosome+'\n')
            genes = all_genes[chromosome]
            for pair in genes:
                name = pair[0]
                sign = ''
                if name in old_names :
                        name = homology[name]
                        if pair[1] == '-':
                            sign = '-'
                        num += 1
                        end_of_chromosome = '$\n'
                        if (not name in coding_table) :
                            print name, 'is not in coding table!'
                            exit()
                        code = coding_table.index(name) + 1 
                        f.write(sign+str(code)+' ')
            f.write(end_of_chromosome)
           
'''
genomes is the dictionary of genes related to chromosomes {chromosome=[(name,strand)]}
code genes with integer numbers
'''
def save_coding_table(coding_table, file):
    i = 1
    with open(file, 'w') as f:
        for gene in coding_table:
            f.write(str(i) + '\t' + gene + '\n')
            i += 1


def reduce_homology(first_specie_genes, second_specie_genes, homology) :
    first_names = []
    second_names = []
    for chromosome in second_specie_genes :
        second_names += [x for x,_ in second_specie_genes[chromosome]]
    for chromosome in first_specie_genes :
        first_names += [x for x,_ in first_specie_genes[chromosome]]
    print second_names[:10]
    for chromosome in first_specie_genes:
        genes = first_specie_genes[chromosome]
        for pair in genes:
            name = pair[0]
            if name in homology.values():
                homolog = [key for key, value in homology.items() if value == name ][0]
                if not homolog in second_names:
                    print name, homolog
                    homology.pop(homolog)

    for chromosome in second_specie_genes:
        genes = second_specie_genes[chromosome]
        for pair in genes:
            name = pair[0]
            if name in homology.keys():
                homolog = homology[name]
                if not homolog in first_names:
                    print name, homolog
                    homology.pop(name)
    print len(homology)
    return homology


def generate_for_grimm() :
    if len(sys.argv) < 6:
        print 'USAGE:', sys.argv[0], 'grimm', 'homology_file', 'first_specie_gff', 'second_specie_gff', 'output_directory'
        exit()
    print utils.get_time()
    print 'parsing homology file...'
    homology = parse_homology(sys.argv[2])
    print utils.get_time()
    print 'parsing genes for the first species...'
    first_specie_genes = parse_genes(sys.argv[3])
    print utils.get_time()
    print 'parsing genes for the second species...'
    second_specie_genes = parse_genes(sys.argv[4])
    #homology = reduce_homology(first_specie_genes, second_specie_genes, homology)
    directory = sys.argv[5]
    utils.create_dir_if_not_exists(directory)
    file = os.path.join(directory,'grimm.input')
    print utils.get_time()
    print 'writing genes to file...'
    coding_table = output_genes('genome1', first_specie_genes, homology, file)
    output_genes_and_rename('genome2', second_specie_genes, homology, coding_table, file)
    coding_table_file = os.path.join(directory,'coding_table.txt')
    print utils.get_time()
    print 'saving coding table...'
    save_coding_table(coding_table, coding_table_file)
    print utils.get_time()
    print 'done.'

def generate_for_grimm_synt() :
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2 :
        print 'you should specify either grimm or grimm_synt parameter'
        exit()

    if sys.argv[1] == 'grimm' :
        generate_for_grimm()
    elif sys.argv[1] == 'grimm_synt' :
        generate_for_grimm_synt()
