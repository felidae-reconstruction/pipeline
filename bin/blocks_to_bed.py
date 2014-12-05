#!/hive/groups/recon/local/bin/python
import sys
import os

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
                name = data[i]+'-'+str(start)+ '-' +str(end)
                hit = data[i]+' '+str(start)+ ' ' +str(end)+ ' ' +name + ' 0 ' +strand+'\n'
                #print i/4, hit
                separate_blocks[i/4].append(hit)
                #print i/4, separate_blocks[i/4]
    print separate_blocks[0][:10]
    print separate_blocks[1][:10]
    return separate_blocks 
            

def write_beds(separate_blocks, output_bed_folder) :
    k = len(separate_blocks)
    for i in range(k):
        name = os.path.join(output_bed_folder,'genome'+str(i+1)+'.bed')
        with open(name,'w') as f:
            for entry in separate_blocks[i]:
                f.write(entry)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print sys.argv[0], 'input_blocks', 'output_bed_folder'
        exit()
    separate_blocks = read_blocks(sys.argv[1])
    write_beds(separate_blocks, sys.argv[2])
