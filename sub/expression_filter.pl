#!/usr/bin/perl-w
# ******************** Software Information *******************
# Version: TSNAD v1.1
# File: expression_filter.pl
# Perl Version: 5.18.2
# Finish time: Octobor, 2018.
# Developer: Jingcheng Wu, Zhan Zhou, Wenyi Zhao 
# Copyright (C) 2018-2019 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
use strict;

my $in=$ARGV[0]; #input mutation file
my $seq=$ARGV[1]; #gene expression file
my $out=$ARGV[2]; # output mutation with expression

open IN, "<$in" or die "cannot open $in:$!";
open SEQ, "<$seq" or die "cannot open $seq:$!";
open OUT, ">$out" or die "cannot open $out:$!";

my %exp;
while (<SEQ>){
	chomp;
	my @line=split/\t/,$_;
	$exp{$line[0]."\t".$line[1]}=$line[7]."\t".$line[8];
}

while (<IN>){
	chomp;
	my @line=split/\t/,$_;
	if ($_=~/##/){
		print OUT"$_\n";
	}
	elsif($_=~/#/){
		print OUT "$_\tRPKM\tTPM\n";
	}
	elsif($exp{$line[3]."\t".$line[17]}){
		my $expression=$exp{$line[3]."\t".$line[17]};
		my @expession=split/\t/,$expression;
		print OUT"$_\t$expression\n" if ($expression>1);
	}
}
