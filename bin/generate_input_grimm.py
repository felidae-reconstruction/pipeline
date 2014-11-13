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
            name = (data[2].split(';')[0]).split('=')[1]
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
    cross_species_homology=dict()
    inter_species_homology=dict()
    with open(homology_file,'r') as f:
        f.readline()
        for line in f:
            data = line.split()
            left = data[0].split(',')
            right = data[1].split(',')
            if right[0] == '*' :
                continue
            for e in left:
                if e == '*' :
                    continue
                #here left and right are the lists of genes. should they names be substituted with the one name? 
                #i.e. subsitute all names in the list e in the left genome with e[0]
                homolog = get_first_element(right)
                cross_species_homology[e] = homolog
                for k in right[1:] :
                    inter_species_homology[k] = homolog
    return cross_species_homology, inter_species_homology

'''
all_genes is the dictionary of {chromosome=[(name,strand)]} for the genome genome_name
homology is the homology relationship {gene1=gene2}. according to this mapping the genes in the genome genome_name are renamed
coding_table is the ordered list [gene]. indexes of the genes will be representations of genes for the grimm_synt input
'''
def rename_and_output_genes(genome_name, all_genes, homology, coding_table, file) :
    with open(file, 'a') as f:
        old_names = list(homology)
        f.write('>name '+genome_name+'\n')
        for chromosome in all_genes :
            #f.write('>'+chromosome+'\n')
            genes = all_genes[chromosome]
            for pair in genes:
                old_name  = pair[0]
                name = old_name
                sign = ''
                if old_name in old_names :
                    name = homology[old_name]
                if pair[1] == '-':
                    sign = '-'
                if not name in coding_table :
                    coding_table.append(name)
                code = coding_table.index(name) + 1 
                f.write(sign+str(code)+' ')
            f.write('$\n')
        return coding_table

def output_genes(genome_name, all_genes, coding_table, inter_species_homology, file) :
    with open(file, 'a') as f:
        f.write('>name '+genome_name+'\n')
        for chromosome in all_genes.keys() :
            #f.write('>'+chromosome+'\n')
            genes = all_genes[chromosome]
            for pair in genes:
                name  = pair[0]
                sign = ''
                if pair[1] == '-':
                    sign = '-'

                #if not name in coding_table :
                #    coding_table.append(name)
                code = 0
                if name in inter_species_homology:
                    homolog = inter_species_homology[name]
                    code = coding_table.index(homolog) + 1
                else :
                    code = coding_table.index(name) + 1 
                f.write(sign+str(code)+' ')
            f.write('$\n')
        return coding_table

'''
genomes is the dictionary of genes related to chromosomes {chromosome=[(name,strand)]}
code genes with integer numbers
'''
def code_genes(genome, inter_species_homology) :
    coding_table = []
    for c in genome:
        for gene in genome[c] :
            if gene[0] in inter_species_homology:
                continue 
            coding_table.append(gene[0])
    return coding_table


def save_coding_table(coding_table, file):
    i = 1
    with open(file, 'w') as f:
        for gene in coding_table: 
            f.write(str(i) + '\t' + gene + '\n')
            i += 1



if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'USAGE:', sys.argv[0], 'homology', 'first_specie_gff', 'second_specie_gff', 'output_directory'
        exit()
    homology, inter_species_homology = parse_homology(sys.argv[1])
    first_specie_genes = parse_genes(sys.argv[2])
    second_specie_genes = parse_genes(sys.argv[3])
    coding_table = code_genes(first_specie_genes, inter_species_homology)
    directory = sys.argv[4]
    utils.create_dir_if_not_exists(directory)
    file = os.path.join(directory,'grimm.input')
    coding_table = output_genes('genome1', first_specie_genes, coding_table, inter_species_homology, file)
    coding_table = rename_and_output_genes('genome2', second_specie_genes, homology, coding_table, file)
    coding_table_file = os.path.join(directory,'coding_table.txt')
    save_coding_table(coding_table, coding_table_file)


