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
            if 'Destination' in line[-1]:
                line = line[:-1]
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

def check_border_for_fission(fission_id, grimm, step, data) :
    for line_prev in grimm[step-1] :
        line_prev = line_prev[:-1]
        data_prev = map(int, line_prev.split())
        data_prev = map(abs, data_prev)             
        if fission_id in data_prev :
            if len(data) == 1:
                if data_prev.index(fission_id) == 0:
                    return data_prev[0:2]
                else:
                    return data_prev[-2:]
            if len(data_prev) > data_prev.index(fission_id) + 1 and (data_prev[data_prev.index(fission_id) + 1] in data): 
                return [data_prev[data_prev.index(fission_id)-1], fission_id]
            elif data_prev.index(fission_id) - 1 > -1 and (data_prev[data_prev.index(fission_id) - 1] in data):
                return [fission_id, data_prev[data_prev.index(fission_id)+1]]
            else :
                print 'data_prev', data_prev
                print 'data', data
                print 'fission_id', fission_id
    return None

def get_list_of_block_ids_from_fissions(fissions, grimm):
    result = []
    for f in fissions:
        step = f[0]
        begin_id = abs(f[1])
        end_id = abs(f[2])
        #appended = False
        for line in grimm[step] :
            line = line[:-1]
            data = map(int, line.split())
            data = map(abs, data)             
            if begin_id in data:
                #appended = True
                result.append(check_border_for_fission(begin_id, grimm, step, data))
            elif end_id in data:
                result.append(check_border_for_fission(end_id, grimm, step, data))
        #if not appended:
        #    print step, begin_id
    return result

def process_fissions(grimm, fissions, all_segments, mgr_macro):
    print 'fissions:', len(fissions)
    filtered_block_ids = list_of_block_ids = get_list_of_block_ids_from_fissions(fissions, grimm)
    print len(list_of_block_ids)

    #note that this makes sense only in case the genome assembly is fragmented
    #this should not be done in case the assembly if chromosome-level
    #list of block ids must contain list of scaffoldseach represented as the list of block ids
    #filtered_block_ids = filter_segments_comprising_separate_scaffolds(list_of_block_ids, mgr_macro, genome_id)
    print len(filtered_block_ids)
    blocks = get_blocks_from_list_of_block_ids(filtered_block_ids, all_segments)
    #print '\n'
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

def filter_segments_comprising_separate_scaffolds(segments, mgr_macro):
    filtered = []
    cnt = 0
    for block in segments:
        exclude = False
        abs_block = map(abs, block)
        for genome in mgr_macro:
            for chromosome in genome:
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


def check_border_for_fusion(fusion_id, grimm, step, data) :
    for line_prev in grimm[step-1] :
        line_prev = line_prev[:-1]
        data_prev = map(int, line_prev.split())
        data_prev = map(abs, data_prev)             
        if fusion_id in data_prev :
            if len(data_prev) == 1:
                if data.index(fusion_id) == 0:
                    return data_prev[0:2]
                else:
                    return data_prev[-2:]
            if data_prev.index(fusion_id) == len(data_prev) - 1:
                return [fusion_id, data[data.index(fusion_id)+1]]
            elif data_prev.index(fusion_id) == 0:
                return [data[data.index(fusion_id)-1], fusion_id]
    return None

def get_list_of_block_ids_from_fusions(fusions, grimm):
    result = []
    for f in fusions:
        step = f[0]
        begin_id = abs(f[1])
        end_id = abs(f[2])
        for line in grimm[step] :
            line = line[:-1]
            data = map(int, line.split())
            data = map(abs, data)
            border = []
            if begin_id in data: 
                result.append(check_border_for_fusion(begin_id, grimm, step, data)) 
            if end_id in data: 
                result.append(check_border_for_fusion(end_id, grimm, step, data))
    return result


def process_fusions(grimm, fusions, all_segments, mgr_macro):
    filtered_block_ids = list_of_block_ids = get_list_of_block_ids_from_fusions(fusions, grimm)
    print len(list_of_block_ids)
    #this was done in case we have the list of block ids that correspond to the whole segments
    #now it's not 
    #filtered_block_ids = filter_segments_comprising_separate_scaffolds(list_of_block_ids, mgr_macro)
    blocks = get_blocks_from_list_of_block_ids(filtered_block_ids, all_segments) 
    print len(blocks)
    return blocks 

def get_list_of_block_ids_from_translocations(translocations, grimm):
    result = []
    for f in translocations:
        step = f[0]
        begin_id = abs(f[1])
        end_id = abs(f[2])
        current_result = []
        for line in grimm[step] :
            begin_index = end_index = None
            line = line[:-1]
            data = map(int, line.split())
            data = map(abs, data)
            if begin_id in data or end_id in data:
                if begin_id in data:
                    current_result.append(begin_id)
                if end_id in data:
                    current_result.append(end_id)
                for line_prev in grimm[step-1]:
                    line_prev = line_prev[:-1]
                    data_prev = map(int, line_prev.split())
                    data_prev = map(abs, data_prev)
                    if begin_id in data_prev:
                        begin_index = data_prev.index(begin_id)
                        if begin_index+1 < len(data_prev) and data_prev[begin_index+1] in data:
                            if begin_index-1 > -1:
                                current_result.append(data_prev[begin_index-1])
                        elif begin_index-1 > -1 and data_prev[begin_index-1] in data:
                            if begin_index+1 < len(data_prev):
                                current_result.append(data_prev[begin_index+1])
                    if end_id in data_prev:
                        end_index = data_prev.index(end_id)
                        if end_index+1 < len(data_prev) and data_prev[end_index+1] in data:
                            if end_index-1 > -1:
                                current_result.append(data_prev[end_index-1])
                        elif end_index-1 > -1 and data_prev[end_index-1] in data:
                            if end_index+1 < len(data_prev):
                                current_result.append(data_prev[end_index+1])
        result.append(current_result)
    return result
                



def process_translocations(grimm, translocations, all_segments):
    print 'translocations', len(translocations)
    list_of_block_ids = get_list_of_block_ids_from_translocations(translocations, grimm)
    print 'list of blocks ids', len(list_of_block_ids)
    blocks = get_blocks_from_list_of_block_ids(list_of_block_ids, all_segments) 
    print 'blocks', len(blocks)
    return blocks 

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
    #fission_segments = process_fissions(grimm, fi, synteny_blocks, mgr_macro)
    #blocks_to_bed.write_beds_with_rgb(fi, fission_segments, 'fissions.bed')
    #length_distr = count_length_distribution(fission_segments)
    #print 'distribution of lengths for fissions:', length_distr 

#    fusion_segments = process_fusions(grimm, fu, synteny_blocks, mgr_macro)
#    print 'fusion segments',len(fusion_segments)
#    blocks_to_bed.write_beds_with_rgb(fu, fusion_segments, 'fusions.bed')
   
    translocation_segments = process_translocations(grimm, t, synteny_blocks)
    blocks_to_bed.write_beds_with_rgb(t, translocation_segments, 'translocations.bed')
