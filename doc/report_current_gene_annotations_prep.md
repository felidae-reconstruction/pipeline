Use the program gene-check developed by Mark

```bash
geneCheck=~markd/compbio/genefinding/GeneTools/bin/x86_64/opt/gene-check
```

* Estimate results the paper Tamazian et.al, 2014

.bb files were obtained from the Dobzhansky center hub for cat assembly annotation

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

* Estimate ensemble gene annotation
Copy from Mark's results

```bash
cd /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/ensemble
cp /hive/groups/recon/projs/felidae/pipeline_data/gene_annotation/FelisCatus/8.0/ensembl80/Felis_catus.Felis_catus_6.2.80.gp ./
cp /hive/groups/recon/projs/felidae/pipeline_data/gene_annotation/FelisCatus/8.0/ensembl80/Felis_catus.Felis_catus_6.2.80.genecheck ./
cp /hive/groups/recon/projs/felidae/pipeline_data/gene_annotation/FelisCatus/8.0/ensembl80/Felis_catus.Felis_catus_6.2.80.genecheck-stats ./
```
Group different isoforms into clusters
```bash
clusterGenes -cds Felis_catus.Felis_catus_6.2.80.cluster_genes no  Felis_catus.Felis_catus_6.2.80.gp
```
Divide clusters into those that contain good and bad predicted genes:
```bash
./geneClusterWithBrokenGenesStats /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/ensemble/Felis_catus.Felis_catus_6.2.80.genecheck /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/ensemble/Felis_catus.Felis_catus_6.2.80.cluster_genes
```
Output:

OK CLUSTERS: 7800 - 40.0184700631 %

PARTIALLY OK CLUSTERS 191 - 0.979939459238 %

BAD CLUSTERS 11499 - 58.9964599046 %

