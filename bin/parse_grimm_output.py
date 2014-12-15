#!/hive/groups/recon/local/bin/python
import sys
import math
import blocks_to_bed

def parse_list_of_steps(file_steps) :
    reversals = []
    translocations = []
    fusions = []
    fissions = []
    all_steps = []
    with open(file_steps) as f:
        for line in f:
            line = line.strip()
            line = line.split(' ') 
            if len(line) < 14 :
                continue
            step_id = int(line[1][:-1])
            first_id = line[6]
            #print first_id
            first_id = int(first_id[1:-1])
            second_id = line[12]
            #print second_id
            second_id = int(second_id[1:-2])
            all_steps.append([first_id, second_id])
            if line[-1] == 'Reversal':
                reversals.append([step_id, first_id, second_id])
            elif line[-1] == 'Translocation':
                translocations.append([step_id, first_id, second_id])
            elif line[-1] == 'Fusion':
                fusions.append([step_id, first_id, second_id])
            elif line[-1] == 'Fission': 
                fissions.append([step_id, first_id, second_id])
    #print all_steps
    all_steps.insert(0,all_steps[0])
    return reversals, translocations, fusions, fissions, all_steps

def parse_grimm_output(grimm_output, steps) :
    grimm = []
    process = False
    with open(grimm_output) as f:
        i = -1
        for line in f:
            line = line.strip()
            if 'Step 0' in line :
                process = True
            if process :
                if 'Step' in  line:
                    #print line
                    i += 1
                    grimm.append([])
                    continue
                data = line.strip().split() 
                for id in data:
                    if id == '$' :
                        continue
                    if (int(id) in steps[i] or -int(id) in steps[i]) or i < len(steps)-1 and (int(id) in steps[i+1] or -int(id) in steps[i+1]):
                        grimm[-1].append(line)
                        break
    return grimm

# genome number is 1-based
# see 'species' file for genome order
# save list of scaffold_id, start, end - for the corresponding genome number
def parse_synteny_blocks(blocks_file, genome_number) :
    blocks = []
    with open(blocks_file) as f:
        for line in f:
            line = line.strip().split()
            if line[0] == '#':
                continue
            start = 1 + (genome_number - 1) * 4 
            blocks.append([line[start], int(line[start+1]), int(line[start+2]), line[start+3]])
    return blocks
            
def get_list_of_block_ids_from_reversals(reversals, grimm):
    result = []
    for r in reversals:
        step = r[0]
        begin_id = r[1]
        end_id = r[2]
        for line in grimm[step] :
            line = line[:-1]
            data = map(int, line.split())
            if -begin_id in data:
                i = data.index(-begin_id)
                j = data.index(-end_id)
                result.append(data[j:i+1])
    return result

def get_blocks_from_list_of_block_ids(reversals_as_list_of_blocks, blocks) :
    scaffolds = []
    for r in reversals_as_list_of_blocks:
        l = []
        for e in r:
            l.append(blocks[abs(e)-1])
        scaffolds.append(l)
    return scaffolds
    
def output_blocks(output_file, blocks):
    with open(output_file, 'w') as f:
        i = 1
        for block in blocks:
            f.write(str(i)+'\n')
            for part in block: 
                part = map(str, part)
                f.write(' '.join(part) + '\n')
            i+=1

def count_length_distribution(blocks) :
    ls = []
    for block in blocks:
        l = 0
        for part in block:
            l += part[2]
        ls.append(l)
    return ls
    
def process_reversals(grimm, reversals, all_blocks) :
    list_of_block_ids = get_list_of_block_ids_from_reversals(reversals, grimm)
    blocks = get_blocks_from_list_of_block_ids(list_of_block_ids, all_blocks)
    return blocks

def get_list_of_block_ids_from_fissions(fissions, grimm):
    result = []
    for f in fissions:
        step = f[0]
        begin_id = f[1]
        end_id = f[2]
        #appended = False
        for line in grimm[step] :
            line = line[:-1]
            data = map(int, line.split())
            if begin_id in data or -begin_id in data:
                #appended = True
                result.append(data)
            elif end_id in data or -end_id in data:
                result.append(data)
        #if not appended:
        #    print step, begin_id
    return result

def process_fissions(grimm, fissions, all_segments, mgr_macro, genome_id):
    print len(fissions)
    list_of_block_ids = get_list_of_block_ids_from_fissions(fissions, grimm)
    print len(list_of_block_ids)

    #note that this makes sense only in case the genome assembly is fragmented
    #this should not be done in case the assembly if chromosome-level
    filtered_block_ids = filter_segments_comprising_separate_scaffolds(list_of_block_ids, mgr_macro, genome_id)
    print len(filtered_block_ids)
    blocks = get_blocks_from_list_of_block_ids(filtered_block_ids, all_segments)
    print '\n'
    print len(blocks)
    return blocks

# chromosomes of each specie consist of syntenic blocks 
# parse file mgr_macro.txt from grimm_synt_output
# returns list of lists. each list inside contains integer number of comprising synteny blocks
def parse_chromosomes(mgr_macro_file) :
    genomes = []
    with open(mgr_macro_file) as f:
        chromosomes = []
        for line in f:
            line = line.strip()
            if '>' in line :
                if len(chromosomes) > 0 :
                    genomes.append(chromosomes)
                    chromosomes = []
                continue
            if '#' in line :
                continue
            chr = line.split()
            chromosomes.append(map(int, chr[:-1]))
        genomes.append(chromosomes)
    for g in genomes:
        print 'g', len(g)
    return genomes

#genome_id in 0 based
def filter_segments_comprising_separate_scaffolds(segments, mgr_macro, genome_id):
    filtered = []
    cnt = 0
    for block in segments:
        exclude = False
        abs_block = map(abs, block)
        for chromosome in mgr_macro[genome_id-1]:
            abs_chromosome = map(abs, chromosome)
            if set(abs_block) == set(abs_chromosome) :
                #print 'block', block, '\n is filtered out from results of fissions because it corresponds to the separate scaffold'
                cnt += 1
                exclude = True
                break
        if not exclude:
            filtered.append(block)
    print cnt, 'blocks comprising separate scaffolds filtered'
    return filtered

def process_fusions(grimm, fusions, all_blocks, mgr_macro, genome_id):
    pass

if __name__ == '__main__':
    if __name__ == '__main__' :
        if len(sys.argv) < 6:
            print 'USAGE:', sys.argv[0], 'grimm.output', 'grimm_steps.output', 'blocks.txt', 'mgr_macro.txt', '1-based_genome_id'
    #params list_of_steps, grimm.output
    r,t,fu,fi,steps = parse_list_of_steps(sys.argv[2])
#steps - steps from 1th to dest
#grimm - strings containing ids ivolved in rearrangements for the steps starting from 0th to dest
#i list in grimm contains strings for i and i-1
    grimm = parse_grimm_output(sys.argv[1], steps) 
    genome_id = int(sys.argv[5])
    synteny_blocks = parse_synteny_blocks(sys.argv[3], genome_id)
    #reversed_segments = process_reversals(grimm, r, synteny_blocks)
    #length_distr = count_length_distribution(reversed_segments)
    #print 'distribution of lengths for reversals:', length_distr 
    #blocks_to_bed.write_beds_with_rgb(r, reversed_segments, 'reversals.bed')

    mgr_macro = parse_chromosomes(sys.argv[4])
    fission_segments = process_fissions(grimm, fi, synteny_blocks, mgr_macro, genome_id)
    blocks_to_bed.write_beds_with_rgb(fi, fission_segments, 'fissions.bed')
    #length_distr = count_length_distribution(fission_segments)
    #print 'distribution of lengths for fissions:', length_distr 
