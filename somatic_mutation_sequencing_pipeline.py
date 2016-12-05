#!/usr/bin/python
# ******************** Software Information *******************
# Version: Somatic_Mutation_Detector 2.0
# File: somatic_mutation_senquencing_pipeline.py
# Python Version: 2.7.11
# Finish time: January, 2016.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2015-2016 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
import datetime
import os
import subfunction

# Read the configure file, and store all the parameters into  
# the hash table
print "\nStep up the sequencing program"
print "This pipeline takes original sequence data (fastq format) as input, calls standrad data processing software (trimmomatic,BWA,etc), and eventually outputs annotated variants\n"
print "Reading the configure file..."
f = open("somatic_mutation_sequencing_parameters.config","r"); # open the configure ile
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
print "inputs_folder: %s"%hash_table['inputs_folder']
print "outputs_folder: %s"%hash_table['outputs_folder']
print "trimmomatic_folder: %s"%hash_table['trimmomatic_folder']
print "bwa_folder:",hash_table['bwa_folder']
print "samtools_folder: %s"%hash_table['samtools_folder']
print "gatk_folder: %s"%hash_table['gatk_folder']
print "picardtools_folder: %s"%hash_table['picardtools_folder']
print "annovar_folder: %s"%hash_table['annovar_folder']
print "soaphla_folder: %s"%hash_table['soaphla_folder']

print "\nProject parameters are:"
print "ref_human_folder: %s"%hash_table['ref_human_folder']
print "ref_1000G_folder: %s"%hash_table['ref_1000G_folder']
print "ref_Mills_folder: %s"%hash_table['ref_Mills_folder']
print "ref_dbsnp_folder: %s"%hash_table['ref_dbsnp_folder']
print "annovarDB_folder: %s"%hash_table['annovarDB_folder']
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
inputs_folder = hash_table['inputs_folder']
outputs_folder = hash_table['outputs_folder']
trimmomatic_folder = hash_table['trimmomatic_folder']
bwa_folder = hash_table['bwa_folder']
samtools_folder = hash_table['samtools_folder']
gatk_folder = hash_table['gatk_folder']
picardtools_folder = hash_table['picardtools_folder']
annovar_folder = hash_table['annovar_folder']
soaphla_folder = hash_table['soaphla_folder']
annovarDB_folder = hash_table['annovarDB_folder']

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
ref_folder.append(hash_table['ref_human_folder']);
ref_folder.append(hash_table['ref_1000G_folder']);
ref_folder.append(hash_table['ref_Mills_folder']);
ref_folder.append(hash_table['ref_dbsnp_folder']);


# -----------------------Main function-------------------------
print "Starting the main function..."
start_time = datetime.datetime.now();
print "Starting time is: %s\n"%start_time

# Reading the folder where project locates
print "All results will be stored in folder %s"%outputs_folder;
folder_name = ["trimmomatic_results","bwa_results","samtools_results","gatk_results","mutect2_results","annovar_results","soaphla_results"]; 

# define all the folder names we may use
for s in folder_name:
    new_path = outputs_folder + s;
    if os.path.exists(new_path): # if the folder has existed, do nothing
        print " Notes: %s has already existed"%new_path;
        continue;
    else:
        os.mkdir(new_path); # generate the folders of intermediate results

fileList = subfunction.getFileList(inputs_folder,"fastq");
# Starting the tools
print "\n\n"
print "*************************************************************************************************************************************"
print "*** Beginning the 1st procedure: fastq file pre-processing...\n"
outputCleanedFile = subfunction.runTrimmomatic(trimmomatic_folder,outputs_folder,fileList,leading,trailing,headcrop,slidingwindow,minlen,typeNum,laneNum,partNum,threadNum); # inputFileFolder means the folder of input Files in next processing step 
print "So far the 1st procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 2nd procedure: BWA mapping to genome reference sequence...\n"
outputSamFiles = subfunction.runBWA(bwa_folder,gatk_folder,ref_folder,outputs_folder,outputCleanedFile,typeNum,laneNum,partNum,threadNum);
print "So far the 2nd procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 3rd procedure: Samtools to rearrange the sequence...\n"
outputIndFiles = subfunction.runSAM(samtools_folder,picardtools_folder,outputs_folder,outputSamFiles,typeNum,laneNum,threadNum);
print "So far the 3rd procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 4th procedure: GATK local realignment around indels...\n"
outputRecalBamFiles = subfunction.runGATK(gatk_folder,ref_folder,outputs_folder,outputIndFiles,typeNum,needRevisedData);
print "So far the 4th procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 5th procedure: MuTect to detect somatic mutation...\n"
outputMutectVcfFiles = subfunction.runMUTECT2(gatk_folder,ref_folder,outputs_folder,outputRecalBamFiles,typeNum);
print "So far the 5th procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 6th procedure: Annovar function annotation...\n"
subfunction.runANN(annovar_folder,annovarDB_folder,outputs_folder,outputMutectVcfFiles,tumor_reads,normal_reads,tumor_f,normal_f,tumor_alt);
print "So far the 6th procedure done.\n\n"

print "*************************************************************************************************************************************"
print "*** Beginning the 7th procedure: HLA parting...\n"
subfunction.runHLA(soaphla_folder,outputs_folder,outputRecalBamFiles,typeNum);
print "So far the 7th procedure done.\n\n"

# Presenting the final results
finish_time = datetime.datetime.now();
print "\nEnding time is: %s"%finish_time
print "The procedure costs time: %s"%(finish_time - start_time);
print "\nCongratulations! This program has finished the required task so far. You can start to plan the next work now.\n"

