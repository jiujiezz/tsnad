#!/usr/bin/perl-w
# ******************** Software Information *******************
# Version: Somatic_Mutation_Detector 2.0
# File: netMHCpan_filter.pl
# Perl Version: 5.18.2
# Finish time: January, 2016.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2015-2016 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
use strict;

my $in1=$ARGV[0]; #input annovar_filter output file
my $in2=$ARGV[1]; #input netMHCpan output file
my $out1=$ARGV[2]; #output binding information
my $out2=$ARGV[3]; #output specific binding information
my $out3=$ARGV[4]; #output mutations with MHC binding
my $out4=$ARGV[5]; #output mutations with specific MHC binding

open IN1, "<$in1" or die "Can not open file $in1:$!";
open IN2, "<$in2" or die "Can not open file $in2:$!";
open OUT1, ">$out1" or die "Can not open file $out1:$!";
open OUT2, ">$out2" or die "Can not open file $out2:$!";
open OUT3, ">$out3" or die "Can not open file $out3:$!";
open OUT4, ">$out4" or die "Can not open file $out4:$!";

my @binding;
my $identity;
my @identity;
my @print_mutation_1;
my @print_mutation_2;

print OUT1 "Position\tHLA\tPeptide\tID\t1-log50k(aff)\tAffinity(nM)\t%Rank\tBindLevel\n";
print OUT2 "Position\tHLA\tPeptide\tID\t1-log50k(aff)\tAffinity(nM)\t%Rank\tBindLevel\n";

my $head=<IN1>;
print OUT3 $head;
print OUT4 $head;

my %record;
while(<IN1>){
	chomp;
	my $line=$_;
	my $mutation=(split /\t/,$line)[9];
	$record{$mutation}=$line; 
}

while(<IN2>){
	chomp;
	my $line=$_;
	my $enst_id;
	$line=~s/<=//;
	my @line=split /\s+/, $line;
	shift @line;
	my $pos=$line[0];
	my $pep=$line[2];
	my $len_pep=length($pep);
	if($line=~/HLA/ && $line=~/WB|SB/){
		next, if($pos>10 || ($pos+$len_pep)<11);
		$line=join "\t", @line;
		$identity=join ":",($line[1],$line[3]);
		if(!grep {$identity eq $_} @identity){
			push @identity, $identity;
		}
		push @binding, $line;
		print OUT1 "$line\n";
		my @mut=split /_/, $line[3];
		foreach my $key(keys %record){
			if(!grep {$key eq $_} @print_mutation_1){
				if($key=~/$mut[0]/ && $key=~/$mut[1]/){
					print OUT3 "$record{$key}\n";
					push @print_mutation_1, $key;
				}
			}
		}
	}
}

foreach my $binding(@binding){
	my @line=split /\t/, $binding;
	$identity=join ":",($line[1],$line[3]);
	if($identity=~/(HLA\S+[A-Z]\d+)[A-Z]$/){
		my $identity_wild=$1;
		if(!grep {$identity_wild eq $_} @identity){
			print OUT2 "$binding\n";
			my @mut=split /_/, $line[3];
			foreach my $key(keys %record){
				if(!grep {$key eq $_} @print_mutation_2){
					if($key=~/$mut[0]/ && $key=~/$mut[1]/){
						print OUT4 "$record{$key}\n";
						push @print_mutation_2, $key;
					}
				}
			}
		}
	}
}


close IN1;
close IN2;
close OUT1;
close OUT2;
close OUT3;
close OUT4;
exit;
