#!/usr/bin/python
# ******************** Software Information *******************
# Version: TSNAD v1.2
# File: subfunction.py
# Python Version: 2.7.11
#<<<<<<< master
# Finish time: May, 2019.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu, Jianan Ren
# Copyright (C) 2016-2019 - College of Pharmaceutical Sciences, 
#=======
# Finish time: November, 2018.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2016-2018 - College of Pharmaceutical Sciences, 
#>>>>>>> master
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
   file_name = f.split("_")[0];  # get file name
   outputName = output_folder + sub_folder + file_name + sub_string;
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


def runTrimmomatic(trimmomatic_tool,outputs_folder,fileList,leading,trailing,headcrop,slidingwindow,minlen,typeNum,laneNum,partNum,threadNum):
 filesNum = len(fileList);
 outputCleanedFile = setOutputFileNames(fileList, '_clean.fastq', outputs_folder, 'trimmomatic_results/',0);
 outputUnpairedFile = setOutputFileNames(fileList, '_unpaired.fastq', outputs_folder, 'trimmomatic_results/',0);
 print " Notes: Multi-processing is applied to speed up the data processing";
 
 loopNum = (laneNum*partNum*typeNum)/2; # trimmomatic processes two files everytime
 print 'loopNum %d'%loopNum
 pool = multiprocessing.Pool();
 for i in range(loopNum):
  command = 'java -jar' + ' ' + trimmomatic_tool + ' ' + 'PE -threads' + ' ' + str(threadNum) + ' -phred33 ' + fileList[2*i] + ' ' + fileList[2*i+1] + ' ' + outputCleanedFile[2*i] + ' ' + outputUnpairedFile[2*i] + ' ' + outputCleanedFile[2*i+1] + ' ' + outputUnpairedFile[2*i+1] + ' ' + 'LEADING:' + str(leading) + ' ' + 'TRAILING:' + str(trailing) + ' ' + 'HEADCROP:' + str(headcrop) + ' '  + 'SLIDINGWINDOW:' + str(slidingwindow) + ' ' + 'MINLEN:' + str(minlen)
  print command
  pool.apply_async(multiprocess1,(fileList[2*i]+' '+fileList[2*i+1],command,));
 pool.close();
 pool.join(); 
 print "\nSub-process(es) done."
 return outputCleanedFile;

 
# Consider normalcell and tumocell as inputs in default, namely typeNum = 2 in default
def setHeaderNames(typeNum,laneNum,version_of_hg):
 sampleHeaderNames = [];
 if laneNum <= 1:
   sampleHeaderNames = [r'@RG\tID:normalcell\tPL:Illumina\tPU:Illumina_XSeq\tLB:normal_'+ version_of_hg  + '\tSM:normal',r'@RG\tID:tumorcell\tPL:Illumina\tPU:Illumina_XSeq\tLB:tumor_GRCh38\tSM:tumor'];
 else:
   for i in range(laneNum):
     header = r'@RG\tID:normalcell'+'-L'+str(i+1)+r'\tPL:Illumina\tPU:Illumina_XSeq\tLB:normal_' + version_of_hg + '\tSM:normal';
     sampleHeaderNames.append(header);
   for i in range(laneNum):
     header = r'@RG\tID:tumorcell'+'-L'+str(i+1)+r'\tPL:Illumina\tPU:Illumina_XSeq\tLB:tumor_' + version_of_hg + '\tSM:tumor';
     sampleHeaderNames.append(header);
 return sampleHeaderNames;

# Long sequence processing in default. pair-end, single reads data is not considered 
def runBWA(bwa_folder,gatk_tool,ref_folder,outputs_folder,inputFiles,typeNum,laneNum,partNum,threadNum,version_of_hg):
 # set header
 sampleHeaderNames = setHeaderNames(typeNum,laneNum,version_of_hg);
 outputSamFiles = setOutputFileNames(inputFiles, '.sam', outputs_folder, 'bwa_results/',partNum);
 filesNum = len(outputSamFiles);
 pool = multiprocessing.Pool();
 inputFiles.sort(); # sort the file name
 print "Blending different parts...\n"
 print " Notes: Multi-processing is applied to speed up the data processing";
 for i in range(filesNum):
  if partNum <= 1:
    command = bwa_folder + 'bwa mem -M -t ' + str(threadNum) + ' -R \''+ sampleHeaderNames[i] + '\' ' + ref_folder[0] + ' ' + inputFiles[i] + ' > ' + outputSamFiles[i];
  else:
    inputFileString = '';
    for j in range(partNum):
      inputFileString = inputFileString + ' ' + inputFiles[i*partNum+j];
    print inputFileString
    command = bwa_folder + 'bwa mem -M -t ' + str(threadNum) + ' -R \''+ sampleHeaderNames[i] + '\' ' + ref_folder[0] + ' ' + inputFileString + ' > ' + outputSamFiles[i];
    pool.apply_async(multiprocess1,(inputFileString,command,));
  print command
 pool.close();
 pool.join();
 outputSamFiles = getFileList(outputs_folder+'bwa_results/','.sam');
 print "\nSub-process(es) done."
 command='rm '+ outputs_folder + 'trimmomatic_results/*';
 #os.system(command)
 return outputSamFiles;
 
def runSAM(samtools_folder,gatk_tool,outputs_folder,inputfiles,typeNum,laneNum,threadNum):
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
    command3 = 'java -Xmx16g -jar' + ' ' + gatk_tool + ' MergeSamFiles ' + inputString + ' OUTPUT=' + outputMergeFiles[i];
    os.system(command3)
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
# command4 = 'java -Xmx16g -jar' + ' ' + gatk_tool + ' MarkDuplicates MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=8000 INPUT=' + inputfiles[i] + ' OUTPUT=' + outputDedupFiles[i] + ' METRICS_FILE=' + outputDedupMetircs[i];
  command4 = 'java -Xmx16g -jar' + ' ' + gatk_tool + ' MarkDuplicates -MAX_FILE_HANDLES_FOR_READ_ENDS_MAP 8000 -I ' + outputMergeFiles[i] + ' -O ' + outputDedupFiles[i] + ' -M ' + outputDedupMetircs[i];
  command5 = samtools_folder + 'samtools'+' index ' + outputDedupFiles[i];
  #pool.apply_async(multiprocess2,(outputMergeFiles[i],command4,command5,));
  os.system(command4);
  os.system(command5);
 pool.close();
 pool.join(); 
 print "\nSub-process(es) done."
 command='rm '+ outputs_folder + 'bwa_results/*';
 #os.system(command)
 return outputDedupFiles;    
 
def runGATK(samtools_folder,gatk_tool,ref_folder,outputs_folder,inputFiles,typeNum,needRevisedData):
 pool = multiprocessing.Pool();
 outputRecalFiles = setOutputFileNames(inputFiles, '_recal.grp', outputs_folder, 'gatk_results/',0);
 outputRecalRevisedFiles = setOutputFileNames(outputRecalFiles, '.report', outputs_folder, 'gatk_results/',0);
 outputRecalBamFiles = setOutputFileNames(inputFiles, '_recal.bam', outputs_folder, 'gatk_results/',0);
 outputRecalsortBamFiles = setOutputFileNames(inputFiles, '_recal_sort.bam', outputs_folder, 'gatk_results/',0);
 pool = multiprocessing.Pool();
 print " Notes: Multi-processing is applied to speed up the data processing";
 for i in range(typeNum):
   command1 = 'java -Xmx16g -jar ' + gatk_tool + ' BaseRecalibrator -R ' + ref_folder[0] + ' -I ' + inputFiles[i] + ' -O ' + outputRecalFiles[i] + ' --known-sites ' + ref_folder[3] + ' --known-sites ' + ref_folder[2] + ' --known-sites ' + ref_folder[1];
   command2 =  'java -Xmx16g -jar ' + gatk_tool + ' GatherBQSRReports -I ' + outputRecalFiles[i] + ' -O ' + outputRecalRevisedFiles[i]
   command3 =  'java -Xmx16g -jar ' + gatk_tool + ' ApplyBQSR -R '+ ref_folder[0] + ' -I ' + inputFiles[i] + ' -bqsr ' + outputRecalRevisedFiles[i] + ' -O ' + outputRecalBamFiles[i]
   command4 = samtools_folder + 'samtools sort -@ 8 ' + outputRecalBamFiles[i] + ' -o ' + outputRecalsortBamFiles[i]
   command5 = samtools_folder + 'samtools index ' + outputRecalsortBamFiles[i]
   os.system(command1);
   os.system(command2);
   os.system(command3);
   os.system(command4);
   os.system(command5);
 pool.close();
 pool.join(); 
 command='rm '+ outputs_folder + 'samtools_results/*';
 os.system(command);
 return outputRecalBamFiles;
 
# MuTect to detect somatic mutation
def runMUTECT2(gatk_tool,ref_folder,outputs_folder,inputFiles,typeNum,tumor_reads,normal_reads,tumor_f,normal_f,tumor_alt):
 print inputFiles
 outputMutectVcfFiles = outputs_folder + 'mutect2_results/' + 'mutect_call.vcf';
 outputMutectVcfadjFiles = outputs_folder + 'mutect2_results/' + 'mutect_call_adj.vcf';
 if typeNum > 1:
   command1 = 'java -Xmx16g -jar ' + gatk_tool + ' Mutect2 -R ' + ref_folder[0] + ' -I ' + inputFiles[0] + ' -normal normal ' + ' -I ' + inputFiles[1] + ' -tumor tumor ' + ' -O ' + outputMutectVcfFiles;
 else:
   print 'Only one type file, cannot make a comparision between normal and tumor genes !';
 print "\n  Processing normal file: %s "%inputFiles[0],"& tumor file: %s"%inputFiles[1];
 os.system(command1);
 current_path = sys.path[0];
 command2 ='perl ' + current_path + '/sub/mutect_filter.pl '+ outputMutectVcfFiles + ' ' + outputMutectVcfadjFiles + ' ' + tumor_reads + ' ' + normal_reads + ' ' + tumor_f + ' ' + normal_f + ' ' + tumor_alt;
 os.system(command2);   
 outputfile = []
 outputfile.append(outputMutectVcfadjFiles)
 return outputfile;


# Function annotation using VEP
def runVEP(vep_folder,outputs_folder,outputMutectVcfadjFiles):
 inputFile = outputMutectVcfadjFiles;
 outputvepFiles = setOutputFileNames(inputFile, '_vep_filtered.txt', outputs_folder, 'vep_results/',0);
 current_path = sys.path[0];
 print "Processing file: %s"%inputFile[0],"\n"
 command = vep_folder + 'vep -i ' +  inputFile[0] + ' -o STDOUT --cache --force_overwrite --tab --offline --use_given_ref --canonical --symbol| ' + vep_folder + 'filter_vep -o STDOUT -filter \"CANONICAL is YES and Consequence is missense_variant\"  --force_overwrite | grep -E \'#|ENSG\' > ' + outputvepFiles[0];
 os.system(command);
 print "VEP processing has been done.\n\n"
 
 return;


# HLA Typing
def runHLA(soaphla_folder,outputs_folder,inputFiles,typeNum):
 pool = multiprocessing.Pool();
 print " Notes: Multi-processing is applied to speed up the data processing";
 for i in range(typeNum):
   command = 'perl ' + soaphla_folder + 'MHC_autopipeline_b37.pl -i ' + inputFiles[i] + ' -od ' + str(outputs_folder+'soaphla_results/') + ' -v hg19';
   pool.apply_async(multiprocess1,(inputFiles[i],command,));
 pool.close();
 pool.join();
 print "\nSub-process(es) done."
 return;

def runkourami(kourami_folder,inputFiles,typeNum):
    pool = multiprocessing.Pool();
    print " Notes: Multi-processing is applied to speed up the data processing";
    for i in range(typeNum):
        p,f = os.path.split(inputFiles[i]);
        file_name = f.split("_")[0];
        os.chdir(p+'/../kourami_results/');
        command1 = 'bash ' + kourami_folder + 'scripts/alignAndExtract_hs38DH.sh ' + file_name + ' ' + inputFiles[i];
        command2 = 'java -jar ' + kourami_folder + 'target/Kourami.jar -d ' + kourami_folder + 'db/ -o ' + file_name + ' ' + file_name + '_on_KouramiPanel.bam';
        os.system(command1)
        os.system(command2)
        os.chdir(p+"/../../")
        print "\nSub-process(es) done."
    return;


# RNA-seq analysis 
def runhisat2(RNA_seq_folder,hisat2_folder,stringtie_tool,samtools_folder,outputs_folder,version_of_hg):
    current_path = sys.path[0];
    inputFile = getFileList(RNA_seq_folder,'fastq.gz')
    p,f = os.path.split(inputFile[0]);
    file_name = f.split("_")[0];
    if 'b37' in version_of_hg:
        command1 = hisat2_folder + 'hisat2 -p 8 --dta -x ' + hisat2_folder + 'grch37/genome -1 ' + inputFile[0] + ' -2 ' + inputFile[1] + ' -S ' +  outputs_folder + 'hisat2_results/' + file_name + '.sam'
        command2 = samtools_folder + 'samtools sort -@ 8 -o ' + outputs_folder + 'hisat2_results/' + file_name + '.bam ' + outputs_folder + 'hisat2_results/' + file_name + '.sam'
        command3 = samtools_folder + 'samtools index ' + outputs_folder + 'hisat2_results/' + file_name + '.bam'
        command4 = stringtie_tool + ' -p 8 -G ' + hisat2_folder + 'Homo_sapiens.GRCh37.87.gtf -A ' + outputs_folder + 'hisat2_results/' + file_name + '.gtf -l ' + file_name + ' ' +  outputs_folder + 'hisat2_results/' +  file_name + '.bam'
        command5 = 'perl ' + current_path + '/sub/expression_filter.pl ' + outputs_folder + 'vep_results/mutect_call_adj_vep_filtered.txt ' + outputs_folder + 'hisat2_results/' + file_name + '.gtf ' + outputs_folder + 'vep_results/mutect_call_adj_vep_filtered_with_expression_' + version_of_hg +'.txt';
    if 'hg38' in version_of_hg:
        command1 = hisat2_folder + 'hisat2 -p 8 --dta -x ' + hisat2_folder + 'grch38/genome -1 ' + inputFile[0] + ' -2 ' + inputFile[1] + ' -S ' +  outputs_folder + 'hisat2_results/' + file_name + '.sam'                                 
        command2 = samtools_folder + 'samtools sort -@ 8 -o ' + outputs_folder + 'hisat2_results/' + file_name + '.bam ' + outputs_folder + 'hisat2_results/' + file_name + '.sam'
        command3 = samtools_folder + 'samtools index ' + outputs_folder + 'hisat2_results/' + file_name + '.bam'
        command4 = stringtie_tool + ' -p 8 -G ' + hisat2_folder + 'Homo_sapiens.GRCh38.96.gtf -A ' + outputs_folder + 'hisat2_results/' + file_name + '.gtf -l ' + file_name + ' ' +  outputs_folder + 'hisat2_results/' +  file_name + '.bam'
        command5 = 'perl ' + current_path + '/sub/expression_filter.pl ' + outputs_folder + 'vep_results/mutect_call_adj_vep_filtered.txt ' + outputs_folder + 'hisat2_results/' + file_name + '.gtf ' + outputs_folder + 'vep_results/mutect_call_adj_vep_filtered_with_expression_' + version_of_hg +'.txt';
    print command1
    print command2
    print command3
    print command4
    print command5
    os.system(command1)
    os.system(command2)
    os.system(command3)
    os.system(command4)
    os.system(command5)
