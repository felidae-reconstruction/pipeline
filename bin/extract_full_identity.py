#!/hive/groups/recon/local/bin/python

import sys
import generate_input_grimm_synt

def parse_bed(constrained_elements):
    l = []
    with open(constrained_elements) as f:
        for line in f:
            data = line.strip().split()
            l.append(data)
    return l

maf = sys.argv[1] 
sizes = sys.argv[2]
constrained_elements = sys.argv[3]
specie_ref = 'FelisCatus'
specie_aligned = 'AcinonyxJubatus'

sizes = generate_input_grimm_synt.parse_all_sizes(sizes)
blocks, species = generate_input_grimm_synt.parse_maf(maf, sizes) 
print 'size of blocks is', len(blocks)
constrained_elements = parse_bed(constrained_elements)
result = []
for e in constrained_elements :
    for b in blocks:
        if specie_aligned in b.get_species() and specie_ref in b.get_species():
            hits = b.hits
            aligned_specie_hits = filter(lambda x: x.specie == specie_aligned, hits)
            ref_specie_hits = filter(lambda x: x.specie == specie_ref, hits)
            #print aligned_specie_hits
            #print ref_specie_hits
            for aligned in aligned_specie_hits:
                for ref in ref_specie_hits:
                    if aligned.sequence == ref.sequence:
                        print aligned.sequence, ref.sequence
                        print
                        result.append(e)

print len(result)
print result[:10]

