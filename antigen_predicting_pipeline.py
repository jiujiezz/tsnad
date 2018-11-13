#!/usr/bin/python
# ******************** Software Information *******************
# Version: TSNAD v1.1
# File: antigen_predicting_pipeline.py
# Python Version: 2.7.11
# Finish time: November, 2018.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2016-2018 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
import datetime
import os,sys

# Read the configure file, and store all the parameters into  
# the hash table
print "\nStep up the antigen predicting program"
print "This pipeline takes data (vcf/txt format) as input\n"
print "Reading the configure file..."
f = open("antigen_predicting_parameters.config","r"); # open the configure file
hash_table = {}; # define a hash table
while 1:
    text = f.readline();
    if text == "":
        break;
    str = text.split(); # split the string
    hash_table[str[0]] = str[1]; # assignment the hash_table
f.close();

# Ouput all the setting parameters in the configure file
print "Printing all the setted parameters...\n"
print "***************************************************************** Parameters ******************************************************************\n"
print "input_file: %s"%hash_table['Input_file']
print "outputs_folder: %s"%hash_table['Outputs_folder']
print "netMHCpan_folder: %s"%hash_table['netMHCpan_folder']
print "A1: %s"%hash_table['A1']
print "A2: %s"%hash_table['A2']
print "B1: %s"%hash_table['B1']
print "B2: %s"%hash_table['B2']
print "C1: %s"%hash_table['C1']
print "C2: %s"%hash_table['C2']
print "peptide_length: %s"%hash_table['peptide_length']
print "***********************************************************************************************************************************************\n"

# Parameter preprocessing
input_file = hash_table['Input_file']
outputs_folder = hash_table['Outputs_folder']
netMHCpan_folder = hash_table['netMHCpan_folder']
A1 = hash_table['A1']
A2 = hash_table['A2']
B1 = hash_table['B1']
B2 = hash_table['B2']
C1 = hash_table['C1']
C2 = hash_table['C2']
peptide_length = hash_table['peptide_length']
if not os.path.exists(outputs_folder): 
    os.mkdir(outputs_folder)
# -----------------------Main function-------------------------
print "Starting the main function for antigen predicting..."
start_time = datetime.datetime.now();
print "Starting time is: %s\n"%start_time

print "All results will be stored in folder %s"%outputs_folder;

# Starting antigen predicting...
print "\n"
print "*************************************************************************************************************************************************"
print "*** Beginning the antigen predicting...\n"

output_21aa_peptides = outputs_folder + '21aa_peptides.txt';

output_netMHCpan_xls = outputs_folder + 'netMHCpan_output.xls';
output_netMHCpan = outputs_folder + 'netMHCpan_output.txt';

output_neoantigen = outputs_folder + 'predicted_neoantigen.txt';

current_path = sys.path[0];
work_path = current_path + '/sub/'; # enter the sub folder

print "Begining protein mutation filtering..."
print "Processing file: %s"%input_file,"\n"
command1 = 'perl ' + work_path + 'protein_mutation_filter.pl ' + input_file + ' ' + output_21aa_peptides + ' ' + work_path + 'protein_sequences_b37.fa';
os.system(command1);
print "Protein mutation filtering done.\n\n"

print "Begining netMHCpan..."
print "Processing file: %s"%output_21aa_peptides,"\n"
command2 = netMHCpan_folder + 'netMHCpan -a HLA-A' + A1 + ',HLA-A' + A2 + ',HLA-B' + B1 + ',HLA-B' + B2 + ',HLA-C' + C1 + ',HLA-C' + C2 + ' -f ' + output_21aa_peptides + ' -s 1 -BA 1 -rth 0.5 -rlt 2.0'  + ' -l ' + peptide_length + ' -xls 1 -xlsfile ' + output_netMHCpan_xls + ' > ' + output_netMHCpan;
os.system(command2);
print "netMHCpan done.\n\n"

print "Begining netMHCpan results filtering..."
print "Processing file: %s"%input_file,"\n"
command3 = 'perl ' + work_path + 'netMHCpan_filter.pl' + ' ' + output_netMHCpan + ' ' + output_neoantigen;
os.system(command3); 
print "netMHCpan results filtering done.\n\n"

# Presenting the final results
finish_time = datetime.datetime.now();
print "\nEnding time is: %s"%finish_time
print "The procedure costs time: %s"%(finish_time - start_time);
print "\nCongratulations! This program has finished the antigen predicting task so far. You can begin to plan the next work now.\n"
