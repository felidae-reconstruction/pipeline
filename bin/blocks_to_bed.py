#!/hive/groups/recon/local/bin/python
import sys
import os
import random
import argparse

#for each specie get its own separate block
def read_blocks(input_blocks) :
    separate_blocks = []
    with open(input_blocks) as f :
        for line in f :
            if not len(line) or line.strip()[0] == '#' :
                continue
            data = line.strip().split()
            data = data[1:]
            k = len(data)/4
            if not len(separate_blocks):
                    separate_blocks = [[] for i in range(k)]
            for i in range(0,k*4,4):
                start = 0
                end = 0
                strand = data[i+3]
                start = int(data[i+1])
                end = int(data[i+1]) + int(data[i+2])
                name = str(start)+ '-' +str(end)
                hit = ' '.join([data[i], str(start), str(end), name, '0', strand])
                separate_blocks[i/4].append(hit)
    return separate_blocks 
            

# input - list of blocks. each element of separate_blocks corresponds to the list of blocks 
# for one specie. each list element in separate_blocks is saved in separate bed file
def write_beds(separate_blocks, output_bed_folder) :
    k = len(separate_blocks)
    for i in range(k):
        name = os.path.join(output_bed_folder,'genome'+str(i+1)+'.bed')
        with open(name,'w') as f:
            for entry in separate_blocks[i]:
                f.write(entry + '\n')
'''
def write_blocks(r, blocks, output_bed_file) :
    k = len(blocks)
    i = 0
    blocks_as_entries = []
    print 'blocks', len(blocks)
    for l in blocks :
        entries = []
        step = 'Step' + str(r[i][0])
        i += 1
        for entry in l:
            print entry
            bed = [entry[0], entry[1], entry[1] + entry[2], step+'-'+str(entry[1]) + '-' + str(entry[2]), '0', entry[3]]
            #entry.insert(-1, str(entry[1]) + '-' + str(entry[2]))
            bed = map(str, bed)
            #old_entry.insert(-1, ' 0 ')
            entries.append(' '.join(bed))
            blocks_as_entries.append(entries)
    with open(output_bed_file,'w') as f:
        for entry in blocks_as_entries:
            f.write(entry + '\n')
'''
    
#all blocks correspond to the one specie
#but each list inside of blocks must be colored in a special random color
def write_beds_with_rgb(r, blocks, output_bed_file) :
    k = len(blocks)
    i = 0
    blocks_as_entries = []
    print 'blocks', len(blocks)
    for l in blocks :
        top_scaffolds = []
        entries = []
        step = 'Step' + str(r[i][0])
        i += 1
        for entry in l:
            bed = [entry[0], entry[1], entry[1] + entry[2], step+'-'+str(entry[1]) + '-' + str(entry[2]), '0', entry[3]]
            #entry.insert(-1, str(entry[1]) + '-' + str(entry[2]))
            bed = map(str, bed)
            #old_entry.insert(-1, ' 0 ')
            entries.append(' '.join(bed))
            top_scaffolds.append(entry[0]+'-'+str(entry[2]))
            blocks_as_entries.append(entries)
        top_scaffolds = sorted(top_scaffolds, key=lambda x: int(x.split('-')[1]), reverse=True)
        #print top_scaffolds[:10]
    with open(output_bed_file,'w') as f:
        for i in range(k):
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            color = str(r)+','+str(g)+','+str(b)
            for entry in blocks_as_entries[i]:
                f.write(entry + ' 0 0 ' + color + ' \n')

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('blocks', help='synteny blocks in grimm synteny format')
    parser.add_argument('output_dir', help='output directory for bed files')
    args = parser.parse_args()
    separate_blocks = read_blocks(args.blocks)
    write_beds(separate_blocks, args.output_dir)
