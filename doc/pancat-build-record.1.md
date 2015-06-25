## 2015-06-24 markd: Ensembl 80 annotations

Ensembl 80 has only FelCat 6.2 so we must map them to FelCat 8.

First convert to genePred, using liftUp to convert UCSC to chromosome names.
````
cd /hive/groups/recon/projs/felidae/pipeline_data/gene_annotation/FelisCatus/8.0/ensembl80
wget -nv ftp://ftp.ensembl.org/pub/release-80/gtf/felis_catus/Felis_catus.Felis_catus_6.2.80.gtf.gz
gtfToGenePred -genePredExt -includeVersion -infoOut=Felis_catus.Felis_catus_6.2.80.info Felis_catus.Felis_catus_6.2.80.gtf.gz stdout | liftUp -type=.gp -extGenePred Felis_catus.Felis_catus_6.2.80.gp /hive/data/genomes/felCat5/jkStuff/ensToUcsc.lift error stdin
genePredCheck db=felCat5 Felis_catus.Felis_catus_6.2.80.gp 
genePredToFakePsl felCat5 Felis_catus.Felis_catus_6.2.80.gp Felis_catus.Felis_catus_6.2.80.psl Felis_catus.Felis_catus_6.2.80.cds
getRnaPred -genePredExt felCat5 Felis_catus.Felis_catus_6.2.80.gp all Felis_catus.Felis_catus_6.2.80.fa
````


map to new assemply
````
pslMap -chainMapFile -swapMap  Felis_catus.Felis_catus_6.2.80.psl /hive/data/genomes/felCat5/bed/blat.felCat8.2014-12-05/felCat5ToFelCat8.over.chain.gz Felis_catus_6.2.80.mapped_8.0.raw.psl -mapInfo=Felis_catus_6.2.80.mapped_8.0.raw.mapinfo
pslCDnaFilter  -filterWeirdOverlapped -maxAligns=1 Felis_catus_6.2.80.mapped_8.0.raw.psl  Felis_catus_6.2.80.mapped_8.0.psl Felis_catus_6.2.80.mapped_8.0.psl
mrnaToGene -quiet -keepInvalid -genePredExt -insertMergeSize=-1 -cdsFile=Felis_catus.Felis_catus_6.2.80.cds Felis_catus_6.2.80.mapped_8.0.psl Felis_catus_6.2.80.mapped_8.0.gp
getRnaPred -genePredExt felCat8 Felis_catus_6.2.80.mapped_8.0.gp all Felis_catus_6.2.80.mapped_8.0.fa
````

                    | seqs	| aligns
             -----------------------
             total:	| 22654	|  23444
        weird over:	|    63	|    133
    drop maxAligns:	|   656	|    790
        kept weird:	|    63	|     63
            kept:	| 22654	|  22654

statistics on mappings
````
pslStats Felis_catus_6.2.80.mapped_8.0.psl  Felis_catus_6.2.80.mapped_8.0.stats
textHistogram -noStar -real -binSize=0.1 -col=7 Felis_catus_6.2.80.mapped_8.0.stats >Felis_catus_6.2.80.mapped_8.0.coverage-histo
````

This is a solid mapping, however there are 431 genes that map with less than
90% coverage.  Suspect this is due to the poor quality of the gene
annotations.  Take a look at the gene feature tests:
````
/hive/groups/recon/local/bin/gene-check --allow-non-coding --genome-seqs=/hive/data/genomes/felCat5/felCat5.2bit Felis_catus.Felis_catus_6.2.80.gp Felis_catus.Felis_catus_6.2.80.genecheck
~markd/compbio/code/pycbio/bin/geneCheckStats  Felis_catus.Felis_catus_6.2.80.genecheck  Felis_catus.Felis_catus_6.2.80.genecheck-stats
/hive/groups/recon/local/bin/gene-check --allow-non-coding --genome-seqs=/hive/data/genomes/felCat8/felCat8.2bit Felis_catus_6.2.80.mapped_8.0.gp Felis_catus_6.2.80.mapped_8.0.genecheck
~markd/compbio/code/pycbio/bin/geneCheckStats  Felis_catus_6.2.80.mapped_8.0.genecheck  Felis_catus_6.2.80.mapped_8.0.genecheck-stats
````
