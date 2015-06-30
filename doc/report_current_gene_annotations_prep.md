Use the program gene-check developed by Mark

```bash
geneCheck=~markd/compbio/genefinding/GeneTools/bin/x86_64/opt/gene-check
geneCheckStats=~markd/compbio/code/pycbio/bin/geneCheckStats
```

* Joan's paper 
annotation is lost

* Estimate results the paper Tamazian et.al, 2014

.bb files were obtained from the Dobzhansky center hub for cat assembly annotation
 http://public.dobzhanskycenter.ru/Hub/cat/fc_genes_*.bb

```bash
genomeSeqs=/hive/groups/recon/projs/felidae/pipeline_data/assemblies/FelisCatus/2014-11-20/Felis_catus_62_rm_trfbig_dm.2bit

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

* Montague - used ensemble gene annotation

* refSeq

```bash
cd /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/refseq
```
use file with ucsc namings 

```bash
genomeSeqs=/hive/data/genomes/felCat5/felCat5.2bit
```

connect to the database. use mysql wrapper

```bash
hgsql -Ne 'select * from refGene' felCat5 | cut -f 2- > Felis_catus_6.2.80.mapped_8.0.gp
```
```bash
${geneCheck} --allow-non-coding --genome-seqs=${genomeSeqs} --details-out=Felis_catus_6.2.80.gene-check-details Felis_catus_6.2.80.gp Felis_catus_6.2.80.gene-check; ${geneCheckStats} Felis_catus_6.2.80.gene-check Felis_catus_6.2.80.gene-check-stats

clusterGenes -cds Felis_catus_6.2.80.cluster-genes no Felis_catus_6.2.80.gp

./geneClusterWithBrokenGenesStats /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/refseq/Felis_catus_6.2.80.gene-check /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/refseq/Felis_catus_6.2.80.cluster-genes 
```
Output: 

OK CLUSTERS: 260 - 67.8851174935 %

PARTIALLY OK CLUSTERS 4 - 1.04438642298 %

BAD CLUSTERS 118 - 30.8093994778 %

* mRNA 
 
Connect to the database and convert to genePred. Don't use bedToGenePred in order to not loose the information
```bash 
hgsql -Ne 'select * from all_mrna' felCat5 | cut -f 2- >Felis_catus_6.2.80.mapped_8.0.psl
hgsql -Ne 'select acc,cds.name from all_mrna rna, gbCdnaInfo gb, cds where (rna.qName=gb.acc) and (gb.cds = cds.id)' felCat5 >Felis_catus.Felis_catus_6.2.80.cds

mrnaToGene -quiet -keepInvalid -genePredExt -insertMergeSize=-1 -cdsFile=Felis_catus.Felis_catus_6.2.80.cds Felis_catus_6.2.80.psl Felis_catus_6.2.80.gp
```
```bash
${geneCheck} --allow-non-coding --genome-seqs=${genomeSeqs} --details-out=Felis_catus_6.2.80.gene-check-details Felis_catus_6.2.80.gp Felis_catus_6.2.80.gene-check; ${geneCheckStats} Felis_catus_6.2.80.gene-check Felis_catus_6.2.80.gene-check-stats

clusterGenes -cds Felis_catus_6.2.80.cluster-genes no Felis_catus_6.2.80.gp

./geneClusterWithBrokenGenesStats /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/mrna/Felis_catus_6.2.80.gene-check /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/mrna/Felis_catus_6.2.80.cluster-genes 
```
 
Output:

OK CLUSTERS: 135 - 22.5 %

PARTIALLY OK CLUSTERS 49 - 8.16666666667 %

BAD CLUSTERS 415 - 69.1666666667 %



