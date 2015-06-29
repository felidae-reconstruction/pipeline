Use the program gene-check developed by Mark

```bash
geneCheck=~markd/compbio/genefinding/GeneTools/bin/x86_64/opt/gene-check
```

Compare results from the paper Tamazian et.al, 2014

```bash
genomeSeqs=/hive/groups/recon/projs/felidae/pipeline_data/assemblies/FelisCatus/2014-11-20/Felis_catus_62_rm_trfbig_dm.2bit
geneCheckStats=~markd/compbio/code/pycbio/bin/geneCheckStats

cd  /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/gaik_annotation/

for specie in dog human cow chimp horse macaque rat mouse; do bigBedToBed fc_genes_${specie}.bb stdout | bedToGenePred stdin fc_genes_${specie}.gp ; sort -k2,2 -k 4,4n fc_genes_${specie}.gp | ${geneCheck} --allow-non-coding --genome-seqs=${genomeSeqs} --details-out=${specie}.gene-check-details stdin ${specie}.gene-check; ${geneCheckStats} ${specie}.gene-check ${specie}.gene-check-stats; done
```

The predictions can overlap. Estimate the gene number counting the overlapped CDS (don't count the UTRs that overlap).

```bash
for specie in dog human cow chimp horse macaque rat mouse; do clusterGenes -cds cluster_genes_${specie}.tab no fc_genes_${specie}.gp; done
```

