#!/usr/bin/perl -w
# ******************** Software Information *******************
# Version: Somatic_Mutation_Detector 2.0
# File: protein_mutation_filter.pl
# Perl Version: 5.18.2
# Finish time: January, 2016.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2015-2016 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
use strict;

my $in=$ARGV[0]; #input annovar_filter output file
my $out1=$ARGV[1]; #output outmembrane protein mutations
my $out2=$ARGV[2]; #output amino acid property changed outmembrane protein mutations
my $out3=$ARGV[3]; #output 21aa peptides including mutation sites  
my $list=$ARGV[4]; #input file: tmhmm_membrane_proteins.txt;
my $amino_acid=$ARGV[5]; #input file: aminoacid.txt;
my $seq=$ARGV[6]; #input file: protein_sequences_b37.fa;

open IN, "<$in" or die "Can not open file $in:$!";
open OUT1, ">$out1" or die "Can not open file $out1:$!";
open OUT2, ">$out2" or die "Can not open file $out2:$!";
open OUT3, ">$out3" or die "Can not open file $out3:$!";
open LIST, "<$list" or die "Can not open file $list:$!";
open AA, "<$amino_acid" or die "Can not open file $amino_acid:$!";
open SEQ, "<$seq" or die "Can not open file $seq:$!";

my $head1=<LIST>;
my %topology;
while(<LIST>){
	chomp;
	my @line=split /\t/, $_;
	my $enst=$line[1];
	my $topology;
	if($line[6]=~/Topology=(\S+)/){
		$topology=$1;
	}
	$topology{$enst}=$topology;
}

my %aa_char;
while(<AA>){
	chomp;
	my $aa=(split /\t/, $_)[0];
	$aa_char{$aa}=(split /\t/, $_)[1];
}

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

close LIST;
close AA;
close SEQ;

my $head2=<IN>;
print OUT1 $head2;
print OUT2 $head2;
chomp $head2;
my @head=split /\t/, $head2;
my ($pos_mut,$pos_type);
foreach my $i(0 .. $#head){
	if($head[$i] eq "AAChange.ensGene"){
		$pos_mut=$i;
	}elsif($head[$i] eq "ExonicFunc.ensGene"){
		$pos_type=$i;
	}
}

while(<IN>){
	chomp;
	my $record=$_;
	my @record=split /\t/, $record;
	my ($enst_id,$wild_aa,$mut_aa,$pos);
	if($record[$pos_type] =~ /nonsynonymous/){
		my @mutation=split /,/,$record[$pos_mut];
		my $match_out=0;
		my $match_aa_char=0;
		foreach my $mutation(@mutation){
			if($mutation=~/(ENST\d+):\S+p.([A-Z]+)(\d+)([A-Z]+)/){
				$enst_id=$1;
				$wild_aa=$2;
				$pos=$3;
				$mut_aa=$4;
				next, if(!$seq{$enst_id});
				my ($id,$seq,$seq_mut,$seq_left,$seq_right);
				if($pos>11){
					$seq_left=substr($seq{$enst_id},$pos-11,10);
				}else{
					$seq_left=substr($seq{$enst_id},0,$pos-1);
				}
				$seq_right=substr($seq{$enst_id},$pos,10);
				$seq=$seq_left.$wild_aa.$seq_right;
				$seq_mut=$seq_left.$mut_aa.$seq_right;
				print OUT3">$gene_name{$enst_id}\_$wild_aa$pos\n$seq\n";
				print OUT3">$gene_name{$enst_id}\_$wild_aa$pos$mut_aa\n$seq_mut\n";
				next, if(!$topology{$enst_id});
				my @outmembrane=split /-/, $topology{$enst_id};
				foreach my $outmembrane(@outmembrane){
					if($outmembrane=~/^o(\d+)/){
						if($pos<$1){
							$match_out=1;
							if($aa_char{$wild_aa} ne $aa_char{$mut_aa}){
								$match_aa_char=1;
							}
						}
					}elsif($outmembrane=~/(\d+)o(\d+)/){
						if($pos>$1 && $pos<$2){
							$match_out=1;
							if($aa_char{$wild_aa} ne $aa_char{$mut_aa}){
								$match_aa_char=1;
							}
						}
					}elsif($outmembrane=~/(\d+)o$/){
						if($pos>$1){
							$match_out=1;
							if($aa_char{$wild_aa} ne $aa_char{$mut_aa}){
								$match_aa_char=1;
							}
						}
					}
				}
			}
		}
		print OUT1 "$record\n", if($match_out==1);
		print OUT2 "$record\n", if($match_aa_char==1);
	}
}
close IN;
close OUT1;
close OUT2;
close OUT3;
exit;
