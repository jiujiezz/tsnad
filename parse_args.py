#!/usr/bin/python
# ******************** Software Information *******************
# Version: TSNAD v2.0.1
# File: parse_args.py
# Python Version: 2.7.11
# Finish time: July, 2021.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu, Jianan Ren
# Copyright (C) 2016-2021 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
# 
# This file define all the sub functions used in somatic_mutation_sequencing_pipeline.py
#

from optparse import OptionParser

def CommandLineParser():
    
    parser=OptionParser()

    print '''
        =====================================================================
                                        TSNAD
        
        TSNAD is an integrated software for tumour-specific neoantigen 
        
        detection from the WGS/WES data of tumor-normal pairs.It could be 
    
        easily used by th following command:

     
        python TSNAD.py -I [dir of WES/WGS] -R [dir of RNA-seq] -V [hg38/b37]
        
        -O [output dir]

        =====================================================================
        '''

    parser.add_option("-I","--input folder *the folder of WGS/WES file*",dest="input")
    parser.add_option("-R","--RNA-seq file folder, [optional]",dest="rna_seq")
    parser.add_option("-V","--version of reference genome, *grch38 or grch37*",dest="version")
    parser.add_option('-O','--OutputDirectory',dest="output")
    return parser.parse_args()
