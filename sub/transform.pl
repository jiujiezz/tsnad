#!/usr/bin/perl-w
# ******************** Software Information *******************
# Version: TSNAD v1.2
# File: transform.pl
# Perl Version: 5.18.2
# Finish time: May, 2019.
# Developer: Jingcheng Wu, Zhan Zhou, Wenyi Zhao 
# Copyright (C) 2016-2019 - College of Pharmaceutical Sciences, 
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
