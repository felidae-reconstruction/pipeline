#!/hive/groups/recon/local/bin/python
import sys
import os
import glob
import utils

class Hit :
    def __init__(self, specie, chr, start, len, sign):
        self.specie = specie
        self.chr = chr
        self.start = start
        self.len = len
        self.sign = sign

    def to_string(self) :
        return self.chr+' '+str(self.start)+' '+str(self.len)+' '+self.sign

class Block:
    def __init__(self, id, hits) :
        self.hits = hits
        self.id = id

    def get_species(self) :
        species = []
        for hit in self.hits:
            species.append(hit.specie)
        return species

    def to_string(self, species) :
        s = [str(self.id)]
        for h in self.hits :
            if (h.specie in species):
                s.append(h.to_string())
        return ' '.join(s)
        

def parse_maf(maf_file, sizes) :
    with open(maf_file) as maf:
        id = 0
        unique_species = set()
        blocks = []
        hits = []
        for line in maf: 
            data = line.strip().split()
            if len(data) and data[0] == 'a':
                if len(hits):
                    id += 1
                    blocks.append(Block(id, hits))
                    hits = []
            if len(data) and data[0] == 's':
               specie, chrom = data[1].split('.')
               start = int(data[2])
               length = int(data[3])
               strand = data[4]
               if strand == '-':
                    start = sizes[specie][chrom] - start - length
               hit = Hit(specie, chrom, start, length, strand)
               hits.append(hit)
               unique_species.add(specie)
        if len(hits) :
            id += 1
            blocks.append(Block(id, hits))
    return blocks, unique_species

def parse_all_sizes(folder):
    files = glob.glob(os.path.join(folder,'*.sizes'))
    sizes = dict()
    for file in files:
        prefix = file.split('.')
        specie = prefix[0].split('/')[-1]
        sizes[specie] = parse_sizes(file)
    print sizes.keys()
    return sizes


def parse_sizes(file) :
    sizes = dict()
    with open(file) as f:
        for line in f:
            data = line.strip().split()
            if not len(data):
                continue
            sizes[data[0]] = int(data[1])
    return sizes

def output_without_repeats(blocks, unique_species, species_to_output, output_file) :
    with open(output_file, 'w') as f:
        for block in blocks:
            if len(block.get_species()) == len(unique_species) and set(block.get_species()) == unique_species :
                f.write(block.to_string(species_to_output)+'\n')
            #else :
            #    print block.to_string()

def parse_species_file(species_file):
    species = []
    with open(species_file) as f:
        for line in f:
            line = line.strip().split(' ')
            if len(line) != 2:
                print 'species file format: genome_id genome_name'
                return []
            species.append(line[1].strip())
    return species

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'USAGE:', sys.argv[0], 'maf_file', 'dir_chrom_sizes', 'output_file', 'species_file'
        exit()
    sizes = parse_all_sizes(sys.argv[2])
    print utils.get_time()
    print 'parsing maf...'
    blocks, unique_species = parse_maf(sys.argv[1], sizes)
    print utils.get_time()
    print 'reading species names...'
    species = parse_species_file(sys.argv[4])
    if len(species) == 0:
        print 'invalid species file!'
        exit()
    print utils.get_time()
    print 'output in grimm_synt format non-repetitive sequences...'
    output_without_repeats(blocks, unique_species, species, sys.argv[3])
    print utils.get_time()
    print 'done.'
