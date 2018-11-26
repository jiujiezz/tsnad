# TSNAD
 
 Neoantigen prediction from WGS or WES.    
   
 Authors: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu.  
 Date: November 2018  
 Version: 1.1  
 License: TSNAD is released under GNU license  

## Introduction  

An integrated software for cancer somatic mutation and tumour-specific neoantigen detection.  

## Requirements
TSNAD uses the following software and libraries:  
  	
1. Trimmomatic  (In Tools/)  
2. bwa  (In Tools/)  
3. samtools  (In Tools/)     
4. [GATK](https://github.com/broadinstitute/gatk/releases/download/4.0.11.0/gatk-4.0.11.0.zip)   
5. [VEP](https://github.com/Ensembl/ensembl-vep/archive/release/94.zip)   
6. [hisat2](http://ccb.jhu.edu/software/hisat2/dl/hisat2-2.1.0-Linux_x86_64.zip)   
7. stringtie  (In Tools/)
8. SOAP-HLA  (In Tools/)
9. NetMHCpan4.0  (In Tools/)
10. JAVA     
11. Python    
12. Perl   
  
1-9 tools are better put in the folder Tools/.   

## Installation of each module
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
	
	uncompress all the downloaded files and put in the same folder (e.g. gatk-\*/b37/)
	
5. VEP

		unzip ensembl-vep-release-*.zip
		cd ensembl-vep-release-*
		perl INSTALL.pl
	
	download the API, download the cache 242 *homo_sapiens_merged_vep_94_GRCh37.tar.gz*.
	
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
		wget ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data/grch37.tar.gz 
		wget ftp://ftp.ensembl.org/pub/grch37/release-94/gtf/homo_sapiens/Homo_sapiens.GRCh37.87.gtf.gz
		tar -xvf grch37.tar.gz
		gunzip Homo_sapiens.GRCh37.87.gtf.gz -d

7. stringtie

		tar -xvf stringtie-*.tar.gz
		
8. SOAP-HLA
		
		unzip SOAP-HLA.zip
		
9. NetMHCpan4.0 
		
		unzip netMHCpan-4.0.zip
		cd netMHCpan-4.0
		vim netMHCpan
		
 	change the *full path* and *tmpdir path* in your own path.


## Usage  

1. configure the file *somatic_mutation_detecting_parameters.config* ,replace the folder path in your own.  

All the input data should end with 'fastq.gz'.

The *RNA_seq_folder* must be empty if you don't have RNA-seq data.  

*hisat2_folder* and *stringtie_tool* are used for RNA-seq analysis. 

	
		trimmomatic_tool /home/biopharm/Software/TSNAD_update-master/Tools/Trimmomatic-0.38/trimmomatic-0.38.jar
		bwa_folder /home/biopharm/Software/TSNAD_update-master/Tools/bwa-0.7.17/
		samtools_folder /home/biopharm/Software/TSNAD_update-master/Tools/samtools-1.9/
		gatk_tool /home/biopharm/Software/TSNAD_update-master/Tools/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar
		VEP_folder /home/biopharm/Software/TSNAD_update-master/Tools/ensembl-vep-release-94/
		hisat2_folder /home/biopharm/Software/TSNAD_update-master/Tools/hisat2-2.1.0/
		stringtie_tool /home/biopharm/Software/TSNAD_update-master/Tools/hisat2-2.1.0/stringtie-1.3.5.Linux_x86_64/stringtie
		soaphla_folder /home/biopharm/Software/TSNAD_update-master/Tools/SOAP-HLA/
		inputs_folder /home/biopharm/Research/TSNAD_update_sample/
		RNA_seq_folder /media/biopharm/data2/NAJ_data/Lab_RNA-seq/S0517021701/
		outputs_folder /home/biopharm/Software/TSNAD_update-master/results/
		ref_human_file /home/biopharm/Software/TSNAD_update-master/Tools/gatk-4.0.11.0/b37/human_g1k_v37.fasta
		ref_1000G_file /home/biopharm/Software/TSNAD_update-master/Tools/gatk-4.0.11.0/b37/1000G_phase1.snps.high_confidence.b37.vcf
		ref_Mills_file /home/biopharm/Software/TSNAD_update-master/Tools/gatk-4.0.11.0/b37/Mills_and_1000G_gold_standard.indels.b37.vcf
		ref_dbsnp_file /home/biopharm/Software/TSNAD_update-master/Tools/gatk-4.0.11.0/b37/dbsnp_138.b37.vcf
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

		A1 02:01
		A2 02:01
		B1 27:05
		B2 15:18
		C1 07:04
		C2 02:02
		Input_file /home/biopharm/Software/TSNAD_update-master/results/vep_results/mutect_call_adj_vep_filtered.txt
		Outputs_folder /home/biopharm/Software/TSNAD_update-master/results/netmhcpan_results/
		netMHCpan_folder /home/biopharm/Software/TSNAD_update-master/Tools/netMHCpan-4.0/
		peptide_length 8,9,10,11

then 

	python antigen_predicting_pipeline.py

## Update log

### V1.0 
1. GUI for neoantigen prediction  
2. Two parts: one for somatic mutation detection, another for HLA-peptide binding prediction.

### V1.1
1. Trimmomatic v0.35 -> v0.38  
2. BWA v0.7.12 -> v0.7.17  
3. Samtools v1.3 -> v1.9  
4. Picard v1.140 -> embedded in GATK 
5. GATK v3.5 -> v4.0.11.0  
6. Annovar -> VEP v94  
7. NetMHCpan v2.8 -> v4.0
 
Add the function of RNA-seq analysis for neoantigen filter.

  
 
