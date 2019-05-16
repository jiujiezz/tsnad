#!/usr/bin/perl -w
# ******************** Software Information *******************
# Version: TSNAD v1.2
# File: protein_mutation_filter.pl
# Perl Version: 5.18.2
# Finish time: May, 2019.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2016-2019 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
use strict;

my $in=$ARGV[0]; #input vep output file
my $out=$ARGV[1]; #output 21aa peptides including mutation sites  
my $seq=$ARGV[2]; #input file: protein_sequences_b37.fa;

open IN, "<$in" or die "Can not open file $in:$!";
open OUT, ">$out" or die "Can not open file $out:$!";
open SEQ, "<$seq" or die "Can not open file $seq:$!";

my %seq;
my %gene_name;
$/=">";
my $head0=<SEQ>;
while(<SEQ>){
	s/\s\n/\n/g;
	chomp;
	my $id;
	my @line=split /\n/, $_;
	my $name=shift @line;
	$id=(split /:/, $name)[1];
	$gene_name{$id}=(split /:/, $name)[3];
	$seq{$id}=join ("", @line);
}
$/="\n";

close SEQ;

my ($position,$pos_mut,$enst);
while(<IN>){
	chomp;
	next if ($_=~/##/);
	if ($_=~/#/){
		my @head=split/\t/,$_;
		foreach my $i(0 .. $#head){
			if($head[$i] eq "Protein_position"){
				$position=$i;		
			}elsif($head[$i] eq "Amino_acids"){
		                $pos_mut=$i;
		       }elsif($head[$i] eq "Feature"){
				$enst=$i
			}
		}
		next;
	}
	my $record=$_;
	my @record=split /\t/, $record;
	my ($enst_id,$wild_aa,$mut_aa,$pos);
	my @mutation=split /\//,$record[$pos_mut];
	$enst_id=$record[$enst];
	$wild_aa=$mutation[0];
	$pos=$record[$position];
	$mut_aa=$mutation[1];
	next, if(!$seq{$enst_id} || length($wild_aa)>1 || !$gene_name{$enst_id});
	my ($id,$seq,$seq_mut,$seq_left,$seq_right);
	if($pos>11){
		$seq_left=substr($seq{$enst_id},$pos-11,10);
	}else{
		$seq_left=substr($seq{$enst_id},0,$pos-1);
	}
	$seq_right=substr($seq{$enst_id},$pos,10);
	$seq=$seq_left.$wild_aa.$seq_right;
	$seq_mut=$seq_left.$mut_aa.$seq_right;
	print OUT">$gene_name{$enst_id}\_$wild_aa$pos\n$seq\n";
	print OUT">$gene_name{$enst_id}\_$wild_aa$pos$mut_aa\n$seq_mut\n";
}
close IN;
close OUT;
exit;
