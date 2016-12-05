#!/usr/bin/perl-w
# ******************** Software Information *******************
# Version: Somatic_Mutation_Detector 2.0
# File: annovar_filter.pl
# Perl Version: 5.18.2
# Finish time: January, 2016.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2015-2016 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
use strict;

my $in=$ARGV[0]; #input annovar output file
my $out1=$ARGV[1]; #output exonic mutations
my $out2=$ARGV[2]; #output missense mutations
my $tumor_reads_cutoff=$ARGV[3];
my $normal_reads_cutoff=$ARGV[4];
my $tumor_f_cutoff=$ARGV[5];
my $normal_f_cutoff=$ARGV[6];
my $tumor_alt_cutoff=$ARGV[7];

open IN, "<$in" or die "Can not open file $in:$!";
open OUT1, ">$out1" or die "Can not open file $out1:$!";
open OUT2, ">$out2" or die "Can not open file $out2:$!";
# if not exist, creat empty files
my $line;
my @line;
my $head=<IN>;
print OUT1 "$head";
print OUT2 "$head";
while(<IN>){
	chomp;
	$line=$_;
	@line=split /\t/, $line;
	if($line=~/PASS/){
		my $chr=$line[0];
		my $start=$line[1];
		my $end=$line[2];
		my $ref=$line[3];
		my $alt=$line[4];
		my $tumor=$line[68];
		my $normal=$line[69];
		my @tumor=split /:/, $tumor;
		my @normal=split /:/, $normal;
		my $tumor_alt=(split /,/, $tumor[1])[1];
		my $normal_alt=(split /,/, $normal[1])[1];
		my $tumor_ref=(split /,/, $tumor[1])[0];
		my $normal_ref=(split /,/, $normal[1])[0];
		my $tumor_reads=$tumor_alt+$tumor_ref;
		my $normal_reads=$normal_alt+$normal_ref;
		my $tumor_f=$tumor_alt/$tumor_reads;
		my $normal_f=$normal_alt/$normal_reads;
		my $gene_name=$line[6];
		my $gene_id=$line[11];
		my $function=$line[10];
		my $exonic_func=$line[13];	
		my $dbsnp=$line[19];
	
		if($function eq "exonic" && $tumor_reads >= $tumor_reads_cutoff && $normal_reads >= $normal_reads_cutoff && $tumor_f >= $tumor_f_cutoff && $tumor_alt >= $tumor_alt_cutoff && $normal_f == $normal_f_cutoff){
			print OUT1 "$line\n";
		}
		if($function eq "exonic" && $exonic_func =~ /nonsynonymous/ && $tumor_reads >= $tumor_reads_cutoff && $normal_reads >= $normal_reads_cutoff && $tumor_f >= $tumor_f_cutoff && $tumor_alt >= $tumor_alt_cutoff && $normal_f == $normal_f_cutoff){
			print OUT2 "$line\n";
		}
	}
}
close IN;
close OUT;
exit;

