Comparing of exon and introns distribution for cat and human ensembl annotations.

```bash
/hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/ensemble/HomoSapiens

wget -nv ftp://ftp.ensembl.org/pub/release-80/gtf/homo_sapiens/Homo_sapiens.GRCh38.80.gtf.gz

gunzip Homo_sapiens.GRCh38.80.gtf.gz 
```
Analogically get ensembl annotation for the mouse.

```bash

cd /hive/groups/recon/projs/felidae_comp/bin

./draw_exons_density /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/ensemble/FelisCatus/Felis_catus.Felis_catus_6.2.80.gtf /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/ensemble/HomoSapiens/Homo_sapiens.GRCh38.80.gtf /hive/groups/recon/projs/felidae_comp/analysis/gene_annotation/ensemble/MusMusculus/Mus_musculus.GRCm38.80.gtf 
```

creates plot_exons_density.pdf in the folder of first .gtf file
