# TSNAD
 
 Neoantigen prediction from WGS or WES.    
   
 Authors: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu, Jianan Ren  
 Date: Sep 2019  
 Version: 2.0  
 License: TSNAD is released under GNU license  
 System: Linux

## Introduction  

An integrated software for cancer somatic mutation and tumour-specific neoantigen detection.  

## Installation and usage

There are two ways to install TSNAD: 

1. installed by docker without any other pre-installed tools (**strongly recommand**, can be used both in linux and windows)

2. installed by github with all required tools installed (only can be used in linux)

### Installed by docker

First, you need to install docker (https://docs.docker.com/)

then, type the following code to install TSNAD:

	docker pull wujingcheng/tsnad:v2.0

it may take several hours to download because of the large size.

### Usage by docker 

You need to enter the TSNAD running enviromont with your path of WES/WGS/RNA-seq as the following command (RNA-seq is not necessary to provide): 
	
	docker run -it -v [dir of WES/WGS]/:/home/tsnad/samples -v [dir of RNA-seq]:/home/tsnad/RNA-seq -v [output dir]:/home/tsnad/results wujingcheng/tsnad:v2.0 /bin/bash	
	
type the following command then the prediction of neoantigen from WES/WGS would start:

	cd /home/tsnad
	
	python TSNAD.py -I samples/ -R RNA-seq/ -V [grch37/grch38] -O results/

All results would be stored in the folder results/, and the final results of neoantigen are stored in the results/deephlapan_results/

### Installed by github

#### Requirements
TSNAD uses the following software and libraries:  
  	
1. Trimmomatic  (In Tools/)  
2. bwa  (In Tools/)  
3. samtools  (In Tools/)     
4. [GATK](https://github.com/broadinstitute/gatk/releases/download/4.0.11.0/gatk-4.0.11.0.zip)   
5. [VEP](https://github.com/Ensembl/ensembl-vep/archive/release/96.zip)   
6. [hisat2](http://ccb.jhu.edu/software/hisat2/dl/hisat2-2.1.0-Linux_x86_64.zip)   
7. stringtie  (In Tools/)
8. SOAP-HLA (for b37, in Tools/)
9. kourami  (for hg38, in Tools/)
10. STAR (In Tools/)
11. arriba (In Tools/)
12. deephlapan 
13. JAVA     
14. Python    
15. Perl   
  
1-10 tools are better put in the folder Tools/.   

#### Installation of each module
1. Trimmomatic   

		unzip Trimmomatic-*.zip

2. bwa

		tar -xjvf bwa-*.tar.bz2
		cd bwa-*
		make

3. samtools
	
		sudo apt-get install libncurses5-dev
		sudo apt-get install libbz2-dev
		sudo apt-get install liblzma-dev
		tar -xjvf samtools-*.tar.bz2
		cd samtools-*
		./configure
		make
		sudo make install

4. GATK

		unzip gatk-*.zip
		sudo apt install openjdk-8-jdk-headless
		
		The necessary files for b37
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/1000G_phase1.snps.high_confidence.b37.vcf.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/1000G_phase1.snps.high_confidence.b37.vcf.idx.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/dbsnp_138.b37.vcf.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/dbsnp_138.b37.vcf.idx.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/Mills_and_1000G_gold_standard.indels.b37.vcf.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/Mills_and_1000G_gold_standard.indels.b37.vcf.idx.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/human_g1k_v37.fasta.gz  
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/human_g1k_v37.fasta.fai.gz  
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/human_g1k_v37.fasta.ann.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/human_g1k_v37.fasta.bwt.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/human_g1k_v37.fasta.amb.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/human_g1k_v37.fasta.pac.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/human_g1k_v37.fasta.sa.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/human_g1k_v37.2bit.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/human_g1k_v37.dict.gz
		
		The necessary files for hg38
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz.tbi
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/dbsnp_146.hg38.vcf.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/dbsnp_146.hg38.vcf.gz.tbi
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz.tbi
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/Homo_sapiens_assembly38.fasta.gz
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/Homo_sapiens_assembly38.fasta.fai
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/Homo_sapiens_assembly38.fasta.64.alt
		wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/Homo_sapiens_assembly38.dict
	
	uncompress all the downloaded files and put them in the same folder (e.g. gatk-*/b37/)
	
	to note, the chromosome name in dbsnp file is different from other files, so we need to transform it as follows :
		
		perl sub/transform.pl dbsnp_138.b37.vcf dbsnp_138.b37_adj.vcf
	
5. VEP

		unzip ensembl-vep-release-*.zip
		cd ensembl-vep-release-*
		perl INSTALL.pl
	
	download the API, download the cache 295 *homo_sapiens_merged_vep_96_GRCh37.tar.gz* for b37, download the cache 296 *homo_sapiens_merged_vep_96_GRCh38.tar.gz* for hg38.
	
	if it is not help, try following step:
		
		cd 
		mkdir src
		cd src
		wget ftp://ftp.ensembl.org/pub/ensembl-api.tar.gz
		wget https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/BioPerl-1.6.924.tar.gz
		tar -xvf ensembl-api.tar.gz
		tar -xvf BioPerl-1.6.924.tar.gz
		
		PERL5LIB=${PERL5LIB}:${HOME}/src/bioperl-1.6.924
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl/modules
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl-compara/modules
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl-variation/modules
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl-funcgen/modules
		export PERL5LIB
		
		sudo perl -MCPAN -e shell
		install Bio::PrimarySeqI
		install DBI
		
6. hisat2

		unzip hisat2-*.zip
		cd hisat2-*
		
		The necessary files for b37
		wget ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data/grch37.tar.gz 
		wget ftp://ftp.ensembl.org/pub/grch37/release-96/gtf/homo_sapiens/Homo_sapiens.GRCh37.87.gtf.gz
		tar -xvf grch37.tar.gz
		gunzip Homo_sapiens.GRCh37.87.gtf.gz -d
		
		The necessary files for hg38
		wget ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data/grch38.tar.gz
		wget ftp://ftp.ensembl.org/pub/release-96/gtf/homo_sapiens/Homo_sapiens.GRCh38.96.gtf.gz
		tar -xvf grch38.tar.gz
		gunzip Homo_sapiens.GRCh38.96.gtf.gz -d

7. stringtie

		tar -xvf stringtie-*.tar.gz

8. SOAP-HLA
	
		unzip SOAP-HLA.zip
		
9. kourami (mvn and bamUtil is needed)
		
		cd kourami*
		mvn install
		scripts/download_panel.sh
		scripts/download_grch38.sh hs38DH
		scripts/download_grch38.sh hs38NoAltDH
		bwa index resources/hs38DH.fa
		bwa index resources/hs38NoAltDH.fa

10. STAR
		
		unzip STAR-master.zip
		cd STAR-master/source
		make STAR
		
		The necessary files for grch37
		wget  ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gtf.gz
		
		The necessary files for grch38
		wget  ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_28/gencode.v28.annotation.gtf.gz

11. Arriba

		tar -xvf arriba_v1.1.0.tar.gz
		cd arriba_v1.1.0 && make

12.DeepHLApan

		unzip deephlapan.zip
		cd deephlapan
		python setup.py install

## Usage  

1. configure the file in the directory */config*, take grch38 as example:

		trimmomatic_tool /notebooks/tsnad/Tools/Trimmomatic-0.38/trimmomatic-0.38.jar
		bwa_folder /notebooks/tsnad/Tools/bwa-0.7.17/
		samtools_folder /notebooks/tsnad/Tools/samtools-1.9/
		gatk_tool /notebooks/tsnad/Tools/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar
		VEP_folder /notebooks/tsnad/Tools/ensembl-vep/
		hisat2_folder /notebooks/tsnad/Tools/hisat2-2.1.0/
		stringtie_tool /notebooks/tsnad/Tools/hisat2-2.1.0/stringtie-1.3.5.Linux_x86_64/stringtie
		soaphla_folder /notebooks/tsnad/Tools/SOAP-HLA/
		kourami_folder  /notebooks/tsnad/Tools/kourami/
		ref_human_file /notebooks/tsnad/Tools/gatk-4.0.11.0/hg38/Homo_sapiens_assembly38.fasta
		ref_1000G_file /notebooks/tsnad/Tools/gatk-4.0.11.0/hg38/1000G_phase1.snps.high_confidence.hg38.vcf
		ref_Mills_file /notebooks/tsnad/Tools/gatk-4.0.11.0/hg38/Mills_and_1000G_gold_standard.indels.hg38.vcf
		ref_dbsnp_file /notebooks/tsnad/Tools/gatk-4.0.11.0/hg38/dbsnp_144.hg38_adj.vcf
		headcrop 10
		leading 3
		minlen 35
		needRevisedData True
		normal_f 0
		normal_reads 6
		slidingwindow 4:15
		threadNum 6
		trailing 3
		tumor_alt 5
		tumor_f 0.05
		tumor_reads 10
		typeNum 2
		laneNum 1
		partNum 2

replace the path of each tool or reference file in your own. The other parameters from *headcrop* to *partNum* should not be changed if 

you don't know their meanings.

2. After configuration, return to the path where *TSNAD.py* located:

		python TSNAD.py -I [dir of WES/WGS] -R [dir of RNA-seq] -V [grch37/grch38] -O [dir of outputs]


## The meaning of parameters in config file
headcrop: Cut the specified number of bases from the start of the read, default 10, used by *trimmomatic*  
leading: Cut bases off the start of a read, if below a threshold quality,default 3, used by *trimmomatic*  
minlen: Drop the read if it is below a specified length, default 35, used by *trimmomatic*  
slidingwindow: Perform a sliding window trimming, cutting once the average quality within the window falls below a threshold, default 4:15, used by *trimmomatic*  
normal_f: The maximum fraction of single nucleotide variant in normal sample, default 0, used for somatic mutation filtering.  
normal_reads: The minimum number of sequence reads in normal sample, default 6, used for somatic mutation filtering.  
tumor_alt: The minimum number of single nucleotide variant in tumor sample, default 5, used for somatic mutation filtering.  
tumor_f: The minimum fraction of single nucleotide variant in tumor sample, default 0.05, used for somatic mutation filtering.  
tumor_reads: The minimum number of sequence reads in tumor sample, default 10, used for somatic mutation filtering.  
typeNum: The number of types of input files(i.e. tumor and normal:2, tumor only :1), default:2. In this tool, it's always 2.  
laneNum: The number of lanes when sequencing, default:1.  
partNum: single-read sequencing:1, paired-end sequencing:2, default:2.  

As the default parameters, the input WGS/WES files in the input directory should be 
		
		normal_L1_R1.fastq
		normal_L1_R2.fastq
		tumor_L2_R1.fastq
		tumor_L2_R2.fastq
		

## Update log
### v2.0
1. provide the neoantigen prediction from indel and gene fusion
2. replace NetMHCpan with DeepHLApan
3. provide the docker version of TSNAD
4. provide the web-service of TSNAD (http://biopharm.zju.edu.cn/tsnad/)

### V1.2
2019.5
1. VEP v94 -> v96
2. Add the selection of hg38 when calling mutations.

### V1.1
2018.11
1. Trimmomatic v0.35 -> v0.38  
2. BWA v0.7.12 -> v0.7.17  
3. Samtools v1.3 -> v1.9  
4. Picard v1.140 -> embedded in GATK 
5. GATK v3.5 -> v4.0.11.0  
6. Annovar -> VEP v94  
7. NetMHCpan v2.8 -> v4.0
8. Add the function of RNA-seq analysis for neoantigen filter.

### V1.0 
2017.4
1. GUI for neoantigen prediction  
2. Two parts: one for somatic mutation detection, another for HLA-peptide binding prediction.


 
