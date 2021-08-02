#!/usr/bin/python
# ******************** Software Information *******************
# Version: TSNAD v2.1
# File: TSNAD.py
# Python Version: 2.7.11
# Finish time: July, 2021.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu, Jianan Ren
# Copyright (C) 2016-2021 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************

import datetime
import os
import subfunction
from parse_args import *

(opt,_)=CommandLineParser()

# Read the configure file, and store all the parameters into  
# the hash table
print "\nStep up the sequencing program"
print "This pipeline takes original sequence data (fastq format) as input, calls standrad data processing software (trimmomatic,BWA,etc), and eventually outputs annotated variants\n"
print "Reading the configure file..."
if 'grch37' in opt.version:
    f = open("config/grch37.config","r"); # open the configure file
if 'grch38' in opt.version:
    f = open("config/grch38.config","r");
hash_table = {}; # define a hash table
while 1:
    text = f.readline();
    if text == "":
        break;
    str = text.split(); # split the string
    hash_table[str[0]] = str[1]; # assignment the hash_table
f.close();

# Ouput all the setting parameters in the configure file
print "Printing all the setted parameters (system and project parameters)...\n"
print "***************************************************************** Parameters ******************************************************************\n"
print "System parameters are:"
print "version_of_hg: %s"%opt.version
print "inputs_folder: %s"%opt.input
print "outputs_folder: %s"%opt.output
print "RNA_seq_folder: %s"%opt.rna_seq
print "trimmomatic_tool: %s"%hash_table['trimmomatic_tool']
print "Optitype_folder: %s"%hash_table['Optitype_folder']
print "bwa_folder:",hash_table['bwa_folder']
print "samtools_folder: %s"%hash_table['samtools_folder']
print "gatk_tool: %s"%hash_table['gatk_tool']
print "star_folder: %s"%hash_table['star_folder']
print "arriba_folder: %s"%hash_table['arriba_folder']

print "\nProject parameters are:"
print "ref_human_file: %s"%hash_table['ref_human_file']
print "ref_1000G_file: %s"%hash_table['ref_1000G_file']
print "ref_Mills_file: %s"%hash_table['ref_Mills_file']
print "ref_dbsnp_file: %s"%hash_table['ref_dbsnp_file']
print "typeNum: %s"%hash_table['typeNum']
print "laneNum: %s"%hash_table['laneNum']
print "partNum: %s"%hash_table['partNum']
print "threadNum: %s"%hash_table['threadNum']
print "needRevisedData:",hash_table['needRevisedData']
print "leading: %s"%hash_table['leading']
print "trailing: %s"%hash_table['trailing']
print "headcrop: %s"%hash_table['headcrop']
print "slidingwindow: %s"%hash_table['slidingwindow']
print "minlen: %s"%hash_table['minlen']
print "tumor_reads: %s"%hash_table['tumor_reads']
print "normal_reads: %s"%hash_table['normal_reads']
print "tumor_f: %s"%hash_table['tumor_f']
print "normal_f: %s"%hash_table['normal_f']
print "tumor_alt: %s"%hash_table['tumor_alt']
print "***********************************************************************************************************************************************\n"

# Parameter preprocessing
version_of_hg = opt.version
inputs_folder = opt.input
outputs_folder = opt.output
RNA_seq_folder = opt.rna_seq
trimmomatic_tool = hash_table['trimmomatic_tool']
Optitype_folder = hash_table['Optitype_folder']
bwa_folder = hash_table['bwa_folder']
samtools_folder = hash_table['samtools_folder']
gatk_tool = hash_table['gatk_tool']
hisat2_folder = hash_table['hisat2_folder']
stringtie_tool = hash_table['stringtie_tool']
VEP_folder = hash_table['VEP_folder']
star_folder = hash_table['star_folder']
arriba_folder = hash_table['arriba_folder']

leading = hash_table['leading']
trailing = hash_table['trailing']
headcrop = hash_table['headcrop']
slidingwindow = hash_table['slidingwindow']
minlen = hash_table['minlen']

typeNum = int(hash_table['typeNum'])
laneNum = int(hash_table['laneNum'])
partNum = int(hash_table['partNum'])
threadNum = int(hash_table['threadNum'])

if hash_table['needRevisedData'] == 'True':
  needRevisedData = True;
else:
  needRevisedData = False;

tumor_reads = hash_table['tumor_reads']
normal_reads = hash_table['normal_reads']
tumor_f = hash_table['tumor_f']
normal_f = hash_table['normal_f']
tumor_alt = hash_table['tumor_alt']

ref_folder = [];
ref_folder.append(hash_table['ref_human_file']);
ref_folder.append(hash_table['ref_1000G_file']);
ref_folder.append(hash_table['ref_Mills_file']);
ref_folder.append(hash_table['ref_dbsnp_file']);


# -----------------------Main function-------------------------
print "Starting the main function..."
start_time = datetime.datetime.now();
print "Starting time is: %s\n"%start_time

if os.path.exists(outputs_folder): # if the folder has existed, do nothing
    print " Notes: %s has already existed"%outputs_folder;
else:
    os.mkdir(outputs_folder);
    
# Reading the folder where project locates
print "All results will be stored in folder %s"%outputs_folder;
if RNA_seq_folder:
    folder_name = ["trimmomatic_results","bwa_results","samtools_results","gatk_results","mutect2_results","vep_results","Optitype_results","star_results","arriba_results","hisat2_results","deephlapan_results"];
else:
    folder_name = ["trimmomatic_results","bwa_results","samtools_results","gatk_results","mutect2_results","vep_results","Optitype_results","deephlapan_results"];


# define all the folder names we may use
for s in folder_name:
    new_path = outputs_folder + "/" + s;
    if os.path.exists(new_path): # if the folder has existed, do nothing
        print " Notes: %s has already existed"%new_path;
        continue;
    else:
        os.mkdir(new_path); # generate the folders of intermediate results

fileList = subfunction.getFileList(inputs_folder,"fastq.gz");

# Starting the tools
print "\n\n"
print "*************************************************************************************************************************************"
print "*** Beginning the 1st procedure: fastq file pre-processing...\n"
outputCleanedFile = subfunction.runTrimmomatic(trimmomatic_tool,outputs_folder,fileList,leading,trailing,headcrop,slidingwindow,minlen,typeNum,laneNum,partNum,threadNum);
# inputFileFolder means the folder of input Files in next processing step 
print "So far the 1st procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 2nd procedure: HLA typing...\n"
subfunction.runOptitype(Optitype_folder,outputs_folder,outputCleanedFile,typeNum);
print "So far the 2nd procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 3rd procedure: BWA mapping to genome reference sequence...\n"
outputSamFiles = subfunction.runBWA(bwa_folder,gatk_tool,ref_folder,outputs_folder,outputCleanedFile,typeNum,laneNum,partNum,threadNum,version_of_hg);
print "So far the 3rd procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 4th procedure: Samtools to rearrange the sequence...\n"
outputIndFiles = subfunction.runSAM(samtools_folder,gatk_tool,outputs_folder,outputSamFiles,typeNum,laneNum,threadNum);
print "So far the 4th procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 5th procedure: GATK local realignment around indels...\n"
outputRecalBamFiles = subfunction.runGATK(samtools_folder,gatk_tool,ref_folder,outputs_folder,outputIndFiles,typeNum,needRevisedData);
print "So far the 5th procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 6th procedure: MuTect to detect somatic mutation...\n"
outputMutectVcfFiles = subfunction.runMUTECT2(gatk_tool,ref_folder,outputs_folder,outputRecalBamFiles,typeNum,tumor_reads,normal_reads,tumor_f,normal_f,tumor_alt);
print "So far the 6th procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 7th procedure: VEP annotation...\n"
outputVEPFiles=subfunction.runVEP(VEP_folder,outputs_folder,outputMutectVcfFiles,version_of_hg);
print "So far the 7th procedure done.\n\n"

if RNA_seq_folder:
    print "*************************************************************************************************************************************"
    print "*** Beginning the 8th procedure: RNA-seq analysis...\n"
    subfunction.runhisat2(RNA_seq_folder,hisat2_folder,stringtie_tool,samtools_folder,outputs_folder,outputVEPFiles,version_of_hg);
    print "So far the 8th procedure done.\n\n"
    print "*** Beginning the 9th procedure: gene-fusion analysis...\n"
    subfunction.runarriba(RNA_seq_folder,star_folder,arriba_folder,outputs_folder,threadNum,version_of_hg)
    print "So far the 9th procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the last procedure: neoantigen predicting...\n"
subfunction.runneoantigen(RNA_seq_folder,outputVEPFiles,outputs_folder,version_of_hg);
print "So far the last procedure done.\n\n"

# Presenting the final results
finish_time = datetime.datetime.now();
print "\nEnding time is: %s"%finish_time
print "The procedure costs time: %s"%(finish_time - start_time);
print "\nCongratulations! This program has finished the required task so far. You can start to plan the next work now.\n"
