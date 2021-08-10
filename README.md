# TSNAD
 
 An integrated pipeline for neoantigen prediction from NGS data.    
   
 Authors: Zhan Zhou, Jingcheng Wu, Xingzheng Lyu, Jianan Ren  
 Date: July 2021  
 Version: 2.0.1  
 License: TSNAD is released under GNU license  
 System: Linux  
 Contact: zhanzhou@zju.edu.cn

## Introduction  

An integrated software for cancer somatic mutation and tumour-specific neoantigen detection.  

## Installation and usage

There are two ways to install TSNAD: 

1. installed by docker without any other pre-installed tools (**strongly recommand**, can be used both in linux and windows)

2. installed by github with all required tools installed (only can be used in linux)

### Installed by docker

First, you need to install docker (https://docs.docker.com/)

then, type the following code to install TSNAD:

	docker pull biopharm/tsnad:latest

it may take several hours to download because of the large size.

### Usage by docker 

You need to enter the TSNAD running enviromont with your path of WES/WGS/RNA-seq as the following command (RNA-seq is not necessary to provide): 
	
	docker run -it -v [dir of WES/WGS]/:/home/tsnad/samples -v [dir of RNA-seq]:/home/tsnad/RNA-seq -v [output dir]:/home/tsnad/results biopharm/tsnad:latest /bin/bash	
	
type the following command then the prediction of neoantigen from WES/WGS would start:

	cd /home/tsnad
	
	bash uncompress.sh
	
	python TSNAD.py -I samples/ -R RNA-seq/ -V [grch37/grch38] -O results/

All results would be stored in the folder results/, and the final results of neoantigen are stored in the results/deephlapan_results/. 

### Installed by github

#### Requirements
TSNAD uses the following software and libraries:  
  	
1. Trimmomatic 0.39 (In Tools/)  
2. BWA 0.7.17 (In Tools/)  
3. SAMtools 1.13 (In Tools/)     
4. [GATK 4.2.0.0](https://github.com/broadinstitute/gatk/releases/download/4.2.0.0/gatk-4.2.0.0.zip) 
5. [VEP 104](https://github.com/Ensembl/ensembl-vep/archive/refs/tags/release/104.3.zip)   
6. [hisat2 2.2.1](https://cloud.biohpc.swmed.edu/index.php/s/oTtGWbWjaxsQ2Ho/download)   
7. Stringtie 2.1.6 (In Tools/)
8. OptiType 1.3.5 (In Tools/)
9. STAR 2.7 (In Tools/)
10. Arriba 1.1.0 (In Tools/)
11. DeepHLApan 1.1 (In Tools/)
12. JAVA 1.8    
13. Python 2.7   
14. Perl 5.22  
  
1-11 tools are better put in the folder Tools/.   

#### Installation of each module
1. Trimmomatic   

		unzip Trimmomatic-*.zip

2. BWA

		tar -xjvf bwa-*.tar.bz2
		cd bwa-*
		make
		
		vim ~/.bashrc
		export PATH=$PATH:/home/tsnad/Tools/bwa-0.7.17/
		source ~/.bashrc

3. SAMtools
	
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
		
		The necessary files for grch37
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
		
		The necessary files for grch38
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
	
	download the API, download the cache *homo_sapiens_merged_vep_104_GRCh37.tar.gz* for grch37, download the cache *homo_sapiens_merged_vep_104_GRCh38.tar.gz* for grch38.
	
	if it is not help, try following step:
		
		cd 
		mkdir src
		cd src
		wget ftp://ftp.ensembl.org/pub/ensembl-api.tar.gz
		wget https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/BioPerl-1.6.924.tar.gz
		tar -xvf ensembl-api.tar.gz
		tar -xvf BioPerl-1.6.924.tar.gz

		PERL5LIB=${PERL5LIB}:${HOME}/src/BioPerl-1.6.924
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl/modules
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl-compara/modules
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl-variation/modules
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl-funcgen/modules
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl-io/modules
		PERL5LIB=${PERL5LIB}:${HOME}/src/ensembl-tools
		export PERL5LIB
		
		sudo perl -MCPAN -e shell
		install Bio::PrimarySeqI
		install DBI
		
6. Hisat2

		unzip hisat2-*.zip
		cd hisat2-*
		
		The necessary files for grch37
		wget https://genome-idx.s3.amazonaws.com/hisat/grch37_genome.tar.gz
		wget http://ftp.ensembl.org/pub/grch37/release-104/gtf/homo_sapiens/Homo_sapiens.GRCh37.87.gtf.gz
		tar -zxvf grch37_genome.tar.gz
		gunzip Homo_sapiens.GRCh37.87.gtf.gz -d
		
		The necessary files for grch38
		wget https://genome-idx.s3.amazonaws.com/hisat/grch38_genome.tar.gz
		wget http://ftp.ensembl.org/pub/release-104/gtf/homo_sapiens/Homo_sapiens.GRCh38.104.gtf.gz
		tar -zxvf grch38_genome.tar.gz
		gunzip Homo_sapiens.GRCh38.104.gtf.gz -d

7. Stringtie

		tar -zxvf stringtie-*.tar.gz

8. OptiType

		unzip OptiType.zip -d OptiType
		
		cd OptiType/glpk-5.0
		./configure
		make && make install
		
		cd ../OptiType/hdf5-1.12.1
		./configure
		make && make install
		
		vim /etc/ld.so.conf
		/usr/local/lib
		/sbin/ldconfig -v
		
		pip install numpy
		pip install pyomo
		pip install pysam
		pip install matplotlib
		pip install tables
		pip install pandas
		pip install future

9. STAR
		
		unzip STAR-master.zip
		cd STAR-master/source
		make STAR
		
		The necessary files for grch37
		wget  ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gtf.gz
		
		The necessary files for grch38
		wget  ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_28/gencode.v28.annotation.gtf.gz

10. Arriba

		tar -xvf arriba_v1.1.0.tar.gz
		cd arriba_v1.1.0 && make

11. DeepHLApan

		unzip deephlapan.zip -d deephlapan
		cd deephlapan
		python setup.py install

### Usage by github  

1. configure the file in the directory */config*, take grch38 as example:

		trimmomatic_tool /home/tsnad/Tools/Trimmomatic-0.39/trimmomatic-0.39.jar
		bwa_folder /home/tsnad/Tools/bwa-0.7.17/
		samtools_folder /home/tsnad/Tools/samtools-1.13/
		gatk_tool /home/tsnad/Tools/gatk-4.2.0.0/gatk-package-4.2.0.0-local.jar
		VEP_folder /home/tsnad/Tools/ensembl-vep/
		hisat2_folder /home/tsnad/Tools/hisat2-2.1.0/
		stringtie_tool /home/tsnad/Tools/hisat2-2.1.0/stringtie-1.3.5.Linux_x86_64/stringtie
		Optitype_folder /home/tsnad/Tools/OptiType/
		star_folder	/home/tsnad/Tools/STAR/
		arriba_folder /home/tsnad/Tools/arriba_v1.1.0/
		ref_human_file /home/tsnad/Tools/gatk-4.2.0.0/grch38/Homo_sapiens_assembly38.fasta
		ref_1000G_file /home/tsnad/Tools/gatk-4.2.0.0/grch38/1000G_phase1.snps.high_confidence.hg38.vcf
		ref_Mills_file /home/tsnad/Tools/gatk-4.2.0.0/grch38/Mills_and_1000G_gold_standard.indels.hg38.vcf
		ref_dbsnp_file /home/tsnad/Tools/gatk-4.2.0.0/grch38/dbsnp_144.hg38_adj.vcf
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

replace the path of each tool or reference file in your own. The other parameters from *headcrop* to *partNum* should not be changed if you don't know their meanings.

2. After configuration, return to the path where *TSNAD.py* located:

		python TSNAD.py -I [dir of WES/WGS] -R [dir of RNA-seq] -V [grch37/grch38] -O [dir of outputs]


## The meaning of parameters in config file
**headcrop**: 		Cut the specified number of bases from the start of the read, default 10, used by *trimmomatic*  
**leading**: 		Cut bases off the start of a read, if below a threshold quality,default 3, used by *trimmomatic*  
**minlen**: 		Drop the read if it is below a specified length, default 35, used by *trimmomatic*  
**slidingwindow**: 	Perform a sliding window trimming, cutting once the average quality within the window falls below a threshold, 				default 4:15, used by *trimmomatic*  
**normal_f**: 		The maximum fraction of single nucleotide variant in normal sample, default 0, used for somatic mutation 				filtering.  
**normal_reads**:	The minimum number of sequence reads in normal sample, default 6, used for somatic mutation filtering.  
**tumor_alt**: 		The minimum number of single nucleotide variant in tumor sample, default 5, used for somatic mutation filtering. 
**tumor_f**: 		The minimum fraction of single nucleotide variant in tumor sample, default 0.05, used for somatic mutation 				filtering.  
**tumor_reads**: 	The minimum number of sequence reads in tumor sample, default 10, used for somatic mutation filtering.  
**typeNum**: 		The number of types of input files(i.e. tumor and normal:2, tumor only :1), default:2. In this tool, it's always 			 2.  
**laneNum**: 		The number of lanes when sequencing, default:1.  
**partNum**: 		Single-read sequencing:1, paired-end sequencing:2, default:2.  

As the default parameters, the input WGS/WES files in the input directory should be 
		
		normal_L1_R1.fastq.gz
		normal_L1_R2.fastq.gz
		tumor_L2_R1.fastq.gz
		tumor_L2_R2.fastq.gz

The samples could be downloaded from following links:

[normal_L1_R1.fastq.gz](https://onedrive.gimhoy.com/sharepoint/aHR0cHM6Ly96anVlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC9iaW9waGFybV96anVfZWR1X2NuL0VTZkdhdXJ2bnpKRWxkMG1uT2ZGQVdvQkc4YjZQZGI1MDlVUFZLMTc1N29CLUE/ZT1mSWZCRlg=.fastq.gz)  
[normal_L1_R2.fastq.gz](https://onedrive.gimhoy.com/sharepoint/aHR0cHM6Ly96anVlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC9iaW9waGFybV96anVfZWR1X2NuL0VXbHprcEl0UkpKSmlRVW01Mkl3VDBVQmVRbzdGcmZqVHVsb0RheDZKUURxX1E/ZT1ZREc1UWw=.fastq.gz)   
[tumor_L2_R1.fastq.gz](https://onedrive.gimhoy.com/sharepoint/aHR0cHM6Ly96anVlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC9iaW9waGFybV96anVfZWR1X2NuL0VZcm1fdElkTUVCR2xYeWw1TGRTQkprQnJnTzFicE0zUmFLamFleVRKOGo5M0E/ZT04clRlTjE=.fastq.gz)   
[tumor_L2_R2.fastq.gz](https://onedrive.gimhoy.com/sharepoint/aHR0cHM6Ly96anVlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC9iaW9waGFybV96anVfZWR1X2NuL0VkaEo1dDNYZFo1TW45eU03ZWRSOEhnQjRobTNNeVVqQUQ0ODBBYlVBeDBtSVE/ZT1XQ3Nlams=.fastq.gz)  
[rna_L1_R1.fastq.gz](https://onedrive.gimhoy.com/sharepoint/aHR0cHM6Ly96anVlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC9iaW9waGFybV96anVfZWR1X2NuL0VWX0w4ODFXb2tCSmtpRTZLOXNIcm1RQkg1Y1VjenpBYUdIWHhKd3BhQjZXZ0E/ZT1POFpBMG4=.fastq.gz)   
[rna_L1_R2.fastq.gz](https://onedrive.gimhoy.com/sharepoint/aHR0cHM6Ly96anVlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC9iaW9waGFybV96anVfZWR1X2NuL0VTSVBWdTNQa2ZwRW9wbGR1LVN6dTU4Qmowb1QxVTNJLU16YV9KOEtvb3FyOGc/ZT1uc0Y1N2g=.fastq.gz)   

To generate useable neoantigen predictions, the minimum depth should be 15X for WGS and 50X for WES, the recommended depth should be 30X for WGS and 100X for WES. For sample with WES tumor/normal data and RNA-seq data, it takes about 50 hours to finish neoantigen prediction in the Ubuntu system with 64G memory and 512G hard disk space.

## Update log

### v2.0.1
2021.07
1. replace SOAP-HLA and Kourami with OptiType
2. the version of each tool is listed as follows:
		
		Trimmomatic 0.39
		BWA 0.7.17
		SAMtools 1.13   
		GATK 4.2.0.0
		VEP 104  
		Hisat2 2.2.1 
		Stringtie 2.1.6
		OptiType 1.3.5
		STAR 2.7
		Arriba 1.1.0
		DeepHLApan 1.1

### v2.0
2019.09
1. provide the neoantigen prediction from indel and gene fusion
2. replace NetMHCpan with DeepHLApan
3. provide the docker version of TSNAD
4. provide the web-service of TSNAD (http://biopharm.zju.edu.cn/tsnad/)

### v1.2
2019.05
1. VEP v94 -> v96
2. Add the selection of grch38 when calling mutations.

### v1.1
2018.11
1. Trimmomatic v0.35 -> v0.38  
2. BWA v0.7.12 -> v0.7.17  
3. SAMtools v1.3 -> v1.9  
4. Picard v1.140 -> embedded in GATK 
5. GATK v3.5 -> v4.0.11.0  
6. Annovar -> VEP v94  
7. NetMHCpan v2.8 -> v4.0
8. Add the function of RNA-seq analysis for neoantigen filter.

### v1.0 
2017.04
1. GUI for neoantigen prediction  
2. Two parts: one for somatic mutation detection, another for HLA-peptide binding prediction.


 
