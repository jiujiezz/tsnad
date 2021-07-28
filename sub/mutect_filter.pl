#!/usr/bin/perl-w
# ******************** Software Information *******************
# Version: TSNAD v2.1
# File: mutect_filter.pl
# Perl Version: 5.26.1
# Latest time: July, 2021.
# Developer: Jingcheng Wu, Zhan Zhou, Wenyi Zhao 
# Copyright (C) 2016-2021 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
use strict;

my $in=$ARGV[0]; #input mutect output file
my $out=$ARGV[1]; #output filtered mutations
my $tumor_reads_cutoff=$ARGV[2];
my $normal_reads_cutoff=$ARGV[3];
my $tumor_f_cutoff=$ARGV[4];
my $normal_f_cutoff=$ARGV[5];
my $tumor_alt_cutoff=$ARGV[6];

open IN, "<$in" or die "cannot open $in:$!";
open OUT, ">$out" or die "cannot open $out:$!";

while (<IN>){
	chomp;
	if ($_=~/#/){
		print OUT"$_\n" 
	}
	else{
		my @line=split/\t/,$_;
		my @tumor=split /:/, $line[10];
		my @normal=split /:/, $line[9];
		my $tumor_alt=(split /,/, $tumor[1])[1];
		my $normal_alt=(split /,/, $normal[1])[1];
		my $tumor_ref=(split /,/, $tumor[1])[0];
		my $normal_ref=(split /,/, $normal[1])[0];
		my $tumor_reads=$tumor_alt+$tumor_ref;
		my $normal_reads=$normal_alt+$normal_ref;
		my $tumor_f=$tumor_alt/$tumor_reads;
		if($tumor_reads >= $tumor_reads_cutoff && $normal_reads >= $normal_reads_cutoff && $tumor_f >= $tumor_f_cutoff && $tumor_alt >= $tumor_alt_cutoff && $normal_alt == 0){
			print OUT "$_\n";
		}
	}
	
}
