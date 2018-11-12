#!/usr/bin/python
# ******************** Software Information *******************
# Version: Somatic_Mutation_Detector 2.0
# File: subfunction.py
# Python Version: 2.7.11
# Finish time: January, 2016.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2015-2016 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
# 
# This file define all the sub functions used in somatic_mutation_sequencing_pipeline.py
#
import os,sys
import multiprocessing


# return a file list which contains the fastq file path
def getFileList(input_folder,substring):
 fileList = [];
 fileNames = os.listdir(input_folder);
 if(len(fileNames) > 0):
   for filename in fileNames:
      if(filename.endswith(substring)):
        fullfilename = os.path.join(input_folder, filename);
        fileList.append(fullfilename);
       
 if(len(fileList) > 0):
   fileList.sort(); # Sort all the file names
 return fileList;

# set output file names
#  For example: output_folder/sub_folder/*_filter.fastq (* is the fileList front names)
def setOutputFileNames(fileList,sub_string,output_folder,sub_folder,flag):
 outputFileList = [];
 fileNum = len(fileList);
 if flag == 0:
  for i in range(fileNum): 
   p,f = os.path.split(fileList[i]);
   file_name = f.split(".")[0];  # get file name
   outputName = output_folder + sub_folder + file_name + sub_string;
   outputFileList.append(outputName); 
 else:
  # This process used to merge different parts
  for i in range(fileNum/flag):
   p,f = os.path.split(fileList[i*flag]);
   file_name = f.split(".")[0];  # get file name
   #outputName = output_folder + sub_folder + file_name + sub_string;
   outputName = output_folder + sub_folder + file_name[0:8] + sub_string; # file_name[0:8] maybe have some problems, one solution is that sample filename must conform to our rules
   outputFileList.append(outputName);
 return outputFileList;

# For all the data processing, multiprocessing method is proposed
# function multiprocess2 is used to process a single task
def multiprocess1(string, command1):
  print "\n  Processing the file: %s"%string;
  os.system(command1);
  return;

# function multiprocess is used to process double sequential tasks
def multiprocess2(string, command1, command2): # string is filename or progressive hints, l is lock control the sequencing output
  print "\n  Processing the file: %s"%string;
  os.system(command1);
  os.system(command2);
  return;

# function multiprocess2 is used to process a trival task
def multiprocess3(string,command1,command2,command3,flag):
  print "\n  Processing the file: %s"%string;
  os.system(command1);
  if flag:
    os.system(command2);
  os.system(command3);
  return;


def runTrimmomatic(trimmomatic_folder,outputs_folder,fileList,leading,trailing,headcrop,slidingwindow,minlen,typeNum,laneNum,partNum,threadNum):
 filesNum = len(fileList);
 outputCleanedFile = setOutputFileNames(fileList, '_clean.fastq', outputs_folder, 'trimmomatic_results/',0);
 outputUnpairedFile = setOutputFileNames(fileList, '_unpaired.fastq', outputs_folder, 'trimmomatic_results/',0);
 print " Notes: Multi-processing is applied to speed up the data processing";
 
 loopNum = (laneNum*partNum*typeNum)/2; # trimmomatic processes two files everytime
 print 'loopNum %d'%loopNum
 pool = multiprocessing.Pool();
 for i in range(loopNum):
  command = 'java -jar' + ' ' + trimmomatic_folder + ' ' + 'PE -threads' + ' ' + str(threadNum) + ' -phred33 ' + fileList[2*i] + ' ' + fileList[2*i+1] + ' ' + outputCleanedFile[2*i] + ' ' + outputUnpairedFile[2*i] + ' ' + outputCleanedFile[2*i+1] + ' ' + outputUnpairedFile[2*i+1] + ' ' + 'LEADING:' + str(leading) + ' ' + 'TRAILING:' + str(trailing) + ' ' + 'HEADCROP:' + str(headcrop) + ' '  + 'SLIDINGWINDOW:' + str(slidingwindow) + ' ' + 'MINLEN:' + str(minlen)
  print command
  pool.apply_async(multiprocess1,(fileList[2*i]+' '+fileList[2*i+1],command,));
 pool.close();
 pool.join(); 
 print "\nSub-process(es) done."
 return outputCleanedFile;

 
# Consider normalcell and tumocell as inputs in default, namely typeNum = 2 in default
def setHeaderNames(typeNum,laneNum):
 sampleHeaderNames = [];
 if laneNum <= 1:
   sampleHeaderNames = [r'@RG\tID:normalcell\tPL:Illumina\tPU:Illumina_XSeq\tLB:normal_GRCh37\tSM:normal',r'@RG\tID:tumorcell\tPL:Illumina\tPU:Illumina_XSeq\tLB:tumor_GRCh37\tSM:tumor'];
 else:
   for i in range(laneNum):
     header = r'@RG\tID:normalcell'+'-L'+str(i+1)+r'\tPL:Illumina\tPU:Illumina_XSeq\tLB:normal_GRCh37\tSM:normal';
     sampleHeaderNames.append(header);
   for i in range(laneNum):
     header = r'@RG\tID:tumorcell'+'-L'+str(i+1)+r'\tPL:Illumina\tPU:Illumina_XSeq\tLB:tumor_GRCh37\tSM:tumor';
     sampleHeaderNames.append(header);
 return sampleHeaderNames;

# Long sequence processing in default. pair-end, single reads data is not considered 
def runBWA(bwa_folder,gatk_folder,ref_folder,outputs_folder,inputFiles,typeNum,laneNum,partNum,threadNum):
 # set header
 sampleHeaderNames = setHeaderNames(typeNum,laneNum);
 outputSamFiles = setOutputFileNames(inputFiles, '.sam', outputs_folder, 'bwa_results/',partNum);
 filesNum = len(outputSamFiles);
 pool = multiprocessing.Pool();
 inputFiles.sort(); # sort the file name
 print "Blending different parts...\n"
 print " Notes: Multi-processing is applied to speed up the data processing";
 for i in range(filesNum):
  if partNum <= 1:
    command = bwa_folder + 'bwa'+' mem -M -t ' + str(threadNum) + ' -R \''+ sampleHeaderNames[i] + '\' ' + ref_folder[0] + ' ' + inputFiles[i] + ' > ' + outputSamFiles[i];
  else:
    inputFileString = '';
    for j in range(partNum):
      inputFileString = inputFileString + ' ' + inputFiles[i*partNum+j];
    print inputFileString
    command = bwa_folder + 'bwa'+' mem -M -t ' + str(threadNum) + ' -R \''+ sampleHeaderNames[i] + '\' ' + ref_folder[0] + ' ' + inputFileString + ' > ' + outputSamFiles[i];
  pool.apply_async(multiprocess1,(inputFileString,command,));
 pool.close();
 pool.join();
 outputSamFiles = getFileList(outputs_folder+'bwa_results/','.sam');
 print "\nSub-process(es) done."
 return outputSamFiles;

 
def runSAM(samtools_folder,picardtools_folder,outputs_folder,inputfiles,typeNum,laneNum,threadNum):
 outputBamFiles = setOutputFileNames(inputfiles, '.bam', outputs_folder, 'samtools_results/',0);
 outputSortedBamFiles = setOutputFileNames(inputfiles, '_sort.bam', outputs_folder, 'samtools_results/',0);
 filesNum = len(outputBamFiles);
 pool = multiprocessing.Pool();
 print " Notes: Multi-processing is applied to speed up the data processing";
 for i in range(filesNum):
   command1 = samtools_folder + 'samtools' + ' view -bS -@ ' + str(threadNum) + ' ' + inputfiles[i] + ' -o ' + outputBamFiles[i];
   command2 = samtools_folder + 'samtools' + ' sort -@ ' + str(threadNum) + ' ' + outputBamFiles[i] + ' -o ' + outputSortedBamFiles[i];
   pool.apply_async(multiprocess2,(inputfiles[i],command1,command2,));
 pool.close();
 pool.join(); 
 print "\nSub-process(es) done."

 # different lanes merging 
 if laneNum > 1:
  print "Merge different lanes because there are more than 1 lanes."
  outputMergeFiles = setOutputFileNames(outputSortedBamFiles, '_sort_merged.bam', outputs_folder, 'samtools_results/',laneNum);
  pool = multiprocessing.Pool();
  print " Notes: Multi-processing is applied to speed up the data processing";
  for i in range(typeNum):
    inputString = '';
    filestring = '';
    for j in range(laneNum):
     inputString = inputString + ' INPUT=' + outputSortedBamFiles[i*laneNum + j];
     filestring = filestring + ' ' + outputSortedBamFiles[i*laneNum + j];
    command3 = 'java -Xmx16g -jar' + ' ' + picardtools_folder + ' MergeSamFiles ' + inputString + ' OUTPUT=' + outputMergeFiles[i];
    pool.apply_async(multiprocess1,(filestring,command3,));
  pool.close();
  pool.join();
  print "\nSub-process(es) done."
 else:
  outputMergeFiles = outputSortedBamFiles;
  
 # duplications removing and sample indexing
 print "Mark duplicates and sample indexing"
 pool = multiprocessing.Pool();
 outputDedupFiles = setOutputFileNames(outputMergeFiles, '_dedup.bam', outputs_folder, 'samtools_results/',0);
 outputDedupMetircs = setOutputFileNames(outputMergeFiles, '_dedup.metrics', outputs_folder, 'samtools_results/',0);
 print " Notes: Multi-processing is applied to speed up the data processing";
 for i in range(typeNum):
  command4 = 'java -Xmx16g -jar' + ' ' + picardtools_folder + ' MarkDuplicates REMOVE_DUPLICATES=false MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=8000 INPUT=' + outputMergeFiles[i] + ' OUTPUT=' + outputDedupFiles[i] + ' METRICS_FILE=' + outputDedupMetircs[i];
  command5 = samtools_folder + 'samtools'+' index ' + outputDedupFiles[i];
  pool.apply_async(multiprocess2,(outputMergeFiles[i],command4,command5,));
 pool.close();
 pool.join(); 
 print "\nSub-process(es) done."
 return outputDedupFiles;

 
def runGATK(gatk_folder,ref_folder,outputs_folder,inputFiles,typeNum,needRevisedData):
 outputRealigerFiles = setOutputFileNames(inputFiles, '_realigner.intervals', outputs_folder, 'gatk_results/',0);
 outputRealnFiles = setOutputFileNames(inputFiles, '_realn.bam', outputs_folder, 'gatk_results/',0);
 pool = multiprocessing.Pool();
 print "\n Step 1: Determining areas which need recompare through Realigner Target Creator & Comparing areas through Indel Realigner..."
 print " Notes: Multi-processing is applied to speed up the data processing";
 for i in range(typeNum):
   command1 = 'java -Xmx16g -jar ' + gatk_folder + ' -T RealignerTargetCreator -R ' + ref_folder[0] + ' -I ' + inputFiles[i] + ' -o ' + outputRealigerFiles[i] + ' -known ' + ref_folder[1] + ' -known ' + ref_folder[2];
   command2 = 'java -Xmx16g -jar ' + gatk_folder + ' -T IndelRealigner -R ' + ref_folder[0] + ' -targetIntervals ' + outputRealigerFiles[i] + ' -I ' + inputFiles[i] + ' -o ' + outputRealnFiles[i] + ' -known ' + ref_folder[1] + ' -known ' + ref_folder[2];
   pool.apply_async(multiprocess2,(inputFiles[i],command1,command2,));
 pool.close();
 pool.join(); 
 print "\n Step 1 is finished. All the sub-process(es) done."
 
 print "\n Step 2: Base Quality Score Recalibration (BQSR)..."
 print "   Substep 2-1: Generate data file that can revise quality according to some known sites using BaseRecalibrator"
 print "   Substep 2-2: Generate revised data file"
 print "   SubStep 2-3: Output a new bam file using toolkit PrintReads"
 outputRecalFiles = setOutputFileNames(outputRealnFiles, '_recal.grp', outputs_folder, 'gatk_results/',0);
 outputRecalRevisedFiles = setOutputFileNames(outputRecalFiles, '_2.grp', outputs_folder, 'gatk_results/',0);
 outputRecalBamFiles = setOutputFileNames(outputRealnFiles, '_recal.bam', outputs_folder, 'gatk_results/',0);
 pool = multiprocessing.Pool();
 print " Notes: Multi-processing is applied to speed up the data processing";
 for i in range(typeNum):
   #Substep 2-1: Generate data file that can revise quality according to some known sites using BaseRecalibrato
   command1 = 'java -Xmx16g -jar ' + gatk_folder + ' -T BaseRecalibrator -R ' + ref_folder[0] + ' -I ' + outputRealnFiles[i] + ' -o ' + outputRecalFiles[i] + ' -knownSites ' + ref_folder[3] + ' -knownSites ' + ref_folder[2] + ' -knownSites ' + ref_folder[1];
   #Substep 2-2: Generate revised data file
   command2 =  'java -Xmx16g -jar ' + gatk_folder + ' -T BaseRecalibrator -R ' + ref_folder[0] + ' -I ' + outputRealnFiles[i] + ' -BQSR ' + outputRecalFiles[i] + ' -o ' + outputRecalRevisedFiles[i]+ ' -knownSites ' + ref_folder[3] + ' -knownSites ' + ref_folder[2] + ' -knownSites ' + ref_folder[1];
   #SubStep 2-3: Output a new bam file using toolkit PrintReads
   command3 = 'java -Xmx16g -jar ' + gatk_folder + ' -T PrintReads -R ' + ref_folder[0] + ' -I ' + outputRealnFiles[i] + ' -BQSR ' + outputRecalFiles[i] + ' -o ' + outputRecalBamFiles[i];
   pool.apply_async(multiprocess3,(outputRealnFiles[i],command1,command2,command3,needRevisedData,));
 pool.close();
 pool.join(); 
 print "\n Step 2 is finished. All the sub-process(es) done.\n"
 
 return outputRecalBamFiles;

 
# MuTect to detect somatic mutation
def runMUTECT2(gatk_folder,ref_folder,outputs_folder,inputFiles,typeNum):
 print inputFiles
 outputMutectVcfFiles = outputs_folder + 'mutect2_results/' + 'mutect_call.vcf';
 if typeNum > 1:
   command = 'java -Xmx16g -jar ' + gatk_folder + ' -T MuTect2 -R ' + ref_folder[0] + ' --dbsnp ' + ref_folder[3] + ' -I:normal ' + inputFiles[0] + ' -I:tumor ' + inputFiles[1] + ' -o ' + outputMutectVcfFiles;
 else:
   print 'Only one type file, cannot make a comparision between normal and tumor genes !';
 print "\n  Processing normal file: %s "%inputFiles[0],"& tumor file: %s"%inputFiles[1];
 os.system(command);
 outputfile = []
 outputfile.append(outputMutectVcfFiles)
 return outputfile;


# Function annotation using Annovar
def runANN(annovar_folder,annovarDB_folder,outputs_folder,outputMutectVcfFiles,tumor_reads,normal_reads,tumor_f,normal_f,tumor_alt):
 inputFile = outputMutectVcfFiles;
 outputAnnoFiles = setOutputFileNames(inputFile, '_anno', outputs_folder, 'annovar_results/',0);
 outputExonMutationFiles = setOutputFileNames(inputFile, '_exonMutation.txt', outputs_folder, 'annovar_results/',0);
 outputMissenseMutationFiles = setOutputFileNames(inputFile, '_missenseMutation.txt', outputs_folder, 'annovar_results/',0);
 current_path = sys.path[0];
 print "Processing file: %s"%inputFile[0],"\n"
 command1 = 'perl ' + str(annovar_folder) + ' ' + inputFile[0] + ' ' + annovarDB_folder + ' -buildver hg19 -out ' + outputAnnoFiles[0] + ' -remove -protocol refGene,ensGene,cytoBand,genomicSuperDups,avsnp144,cosmic70,nci60,esp6500siv2_all,1000g2015aug_all,dbnsfp30a -operation g,g,r,r,f,f,f,f,f,f -nastring . -vcfinput';
 os.system(command1);
 print "Annovar processing has been done.\n\n"
 
 input_file = outputs_folder + 'annovar_results/' + 'mutect_call_anno.hg19_multianno.txt';  # This name is setted manually since the annovar outputing names are settled.
 print "Processing file: %s"%input_file
 command2 = 'perl ' + current_path + '/sub/annovar_filter.pl ' + input_file + ' ' + outputExonMutationFiles[0] + ' ' + outputMissenseMutationFiles[0] + ' '  + str(tumor_reads) + ' ' + str(normal_reads) + ' ' + str(tumor_f) + ' ' + str(normal_f) + ' ' + str(tumor_alt);
 os.system(command2);
 print "Annovar filtering has been done.\n\n"
 return;

 
# HLA Typing
def runHLA(soaphla_folder,outputs_folder,inputFiles,typeNum):
 pool = multiprocessing.Pool();
 print " Notes: Multi-processing is applied to speed up the data processing";
 for i in range(typeNum):
   command = 'perl ' + soaphla_folder + ' -i ' + inputFiles[i] + ' -od ' + str(outputs_folder+'soaphla_results/') + ' -v hg19';
   pool.apply_async(multiprocess1,(inputFiles[i],command,));
 pool.close();
 pool.join();
 print "\nSub-process(es) done."
 return;
