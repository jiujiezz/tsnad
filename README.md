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

1. installed by docker without any other pre-installed tools (strongly recommand)

2. installed by github with all required tools installed 

### Installed by docker

First, you need to install docker (https://docs.docker.com/)

then, type the following code to install TSNAD:

	docker pull wujingcheng/tsnad:v2.0

it may take several hours to download because of the large size.

### usage by docker 

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
10. NetMHCpan4.0  (In Tools/)
11. JAVA     
12. Python    
13. Perl   
  
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
		
10. NetMHCpan4.0 
		
		unzip netMHCpan-4.0.zip
		cd netMHCpan-4.0
		vim netMHCpan
		
 	change the *full path* and *tmpdir path* to your own path.


## Usage  

1. configure the file *somatic_mutation_detecting_parameters.config* ,replace the folder path in your own.  

All the input data should end with 'fastq.gz'.

The *RNA_seq_folder* must be empty if you don't have RNA-seq data.  

*hisat2_folder* and *stringtie_tool* are used for RNA-seq analysis. 


		version_of_hg hg38
		trimmomatic_tool /media/biopharm/data1/TSNAD_update-master/Tools/Trimmomatic-0.38/trimmomatic-0.38.jar
		bwa_folder /media/biopharm/data1/TSNAD_update-master/Tools/bwa-0.7.17/
		samtools_folder /media/biopharm/data1/TSNAD_update-master/Tools/samtools-1.9/
		gatk_tool /media/biopharm/data1/TSNAD_update-master/Tools/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar
		VEP_folder /media/biopharm/data1/TSNAD_update-master/Tools/ensembl-vep-release-96/
		hisat2_folder /media/biopharm/data1/TSNAD_update-master/Tools/hisat2-2.1.0/
		stringtie_tool /media/biopharm/data1/TSNAD_update-master/Tools/hisat2-2.1.0/stringtie-1.3.5.Linux_x86_64/stringtie
		soaphla_folder /media/biopharm/data1/TSNAD_update-master/Tools/SOAP-HLA/
		kourami_folder  /media/biopharm/data1/TSNAD_update-master/Tools/kourami/
		inputs_folder /home/biopharm/renjianan/
		RNA_seq_folder /media/biopharm/data2/NAJ_data/Lab_RNA-seq/S0517021701/
		outputs_folder /media/biopharm/data1/TSNAD_update-master/results/
		ref_human_file /media/biopharm/data1/TSNAD_update-master/Tools/gatk-4.0.11.0/hg38/Homo_sapiens_assembly38.fasta
		ref_1000G_file /media/biopharm/data1/TSNAD_update-master/Tools/gatk-4.0.11.0/hg38/1000G_phase1.snps.high_confidence.hg38.vcf
		ref_Mills_file /media/biopharm/data1/TSNAD_update-master/Tools/gatk-4.0.11.0/hg38/Mills_and_1000G_gold_standard.indels.hg38.vcf
		ref_dbsnp_file /media/biopharm/data1/TSNAD_update-master/Tools/gatk-4.0.11.0/hg38/dbsnp_144.hg38_adj.vcf
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
		

then 

	python  somatic_mutation_detecting_pipeline.py

2. configure the file *antigen_predicting_parameters.config* ,

		version_of_hg hg38
		A1 02:01
		A2 02:01
		B1 27:05
		B2 15:18
		C1 07:04
		C2 02:02
		Input_file /media/biopharm/data1/TSNAD_update-master/results/vep_results/mutect_call_adj_vep_filtered.txt
		Outputs_folder /media/biopharm/data1/TSNAD_update-master/results/netmhcpan_results/
		netMHCpan_folder /media/biopharm/data1/TSNAD_update-master/Tools/netMHCpan-4.0/
		peptide_length 8,9,10,11

then 

	python antigen_predicting_pipeline.py

## Update log

### V1.0 
2017.4
1. GUI for neoantigen prediction  
2. Two parts: one for somatic mutation detection, another for HLA-peptide binding prediction.

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

### V1.2
2019.5
1. VEP v94 -> v96
2. Add the selection of hg38 when calling mutations.

 
