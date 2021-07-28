#!/usr/bin/perl-w
# ******************** Software Information *******************
# Version: TSNAD v2.1
# File: transform.pl
# Perl Version: 5.26.1
# Latest time: July, 2021.
# Developer: Jingcheng Wu, Zhan Zhou, Wenyi Zhao 
# Copyright (C) 2016-2021 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
use strict;

my $in=$ARGV[0]; #input dbsnp file 
my $out=$ARGV[1]; # output adjusted dbsnp file 

open IN, "<$in" or die "cannot open $in:$!";
open OUT, ">$out" or die "cannot open $out:$!";

while (<IN>){
	chomp;
	if ($_=~/#/){
		print OUT"$_\n";
	}
	else{
		my @line=split/\t/,$_;
		$line[0]='chr'.$line[0];
		my $line=join "\t",@line;
		print OUT"$line\n";
	}
}
