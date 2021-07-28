#!/usr/bin/perl -w
# ******************** Software Information *******************
# Version: TSNAD v2.1
# File: protein_mutation_filter_deephlapan.pl
# Perl Version: 5.26.1
# Latest time: July, 2021.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2016-2021 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
use strict;

my $in=$ARGV[0]; #input vep output file
my $out1=$ARGV[1];#output outmembrane protein mutations
my $out2=$ARGV[2];#output amimo acid property changed outmembrane protein mutations
my $out3=$ARGV[3];#output 21aa peptides including mutation sites 
my $list=$ARGV[4];
my $amino_acid=$ARGV[5];
my $hla=$ARGV[6];
my $version=$ARGV[7];
my $seq=$ARGV[8]."/sub/protein_sequences_".$version.".fa"; #input file: protein_sequences_b37.fa;

open IN, "<$in" or die "Can not open file $in:$!";
open OUT1, ">$out1" or die "Can not open file $out1:$!";
open OUT2, ">$out2" or die "Can not open file $out2:$!";
open OUT3, ">$out3" or die "Can not open file $out3:$!";
open LIST, "<$list" or die "Can not open file $list:$!";
open AA, "<$amino_acid" or die "Can not open file $amino_acid:$!";
open SEQ, "<$seq" or die "Can not open file $seq:$!";
open HLA, "<$hla" or die "Can not open file $hla:$!";

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

my @hla;
my $num=0;
while (<HLA>){
	chomp;
	my @line=split/\t/,$_;
	my $hla=join":",(split/:/,$line[0])[0,1];
	$hla=~s/\*//;
	$hla='HLA-'.$hla;
	push @hla,$hla;
	$num++;
	last if ($num==6);	
}

print OUT3"Annotation,HLA,peptide\n";
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

my ($position,$pos_mut,$enst,$type);
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
			}elsif($head[$i] eq "Consequence"){
				$type=$i
			}
		}
		next;
	}
	
	my ($enst_id,$wild_aa,$mut_aa,$pos,$left_pos,$right_pos);
	my $record=$_;
	my $match_out=0;
    my $match_aa_char=0;
	my @record=split /\t/, $record;
	$enst_id=$record[$enst];
	my $mutation_type=$record[$type];
	if ($mutation_type=~/missense_variant/){
		my @mutation=split /\//,$record[$pos_mut];
		$wild_aa=$mutation[0];
		$pos=$record[$position];
		$mut_aa=$mutation[1];
		next, if(!$seq{$enst_id} || length($wild_aa)>1 || !$gene_name{$enst_id});
		my ($id,$seq,$seq_mut,$seq_left,$seq_right);
		$seq_right=substr($seq{$enst_id},$pos,10);
		if($pos>=11){
			$seq_left=substr($seq{$enst_id},$pos-11,10);
			$seq=$seq_left.$wild_aa.$seq_right;
			$seq_mut=$seq_left.$mut_aa.$seq_right;
			$seq_mut=~s/\*//;
			for my $i (8,9,10,11){
				my $pos1=$i;
				for my $j (11-$i..10){
					foreach my $hla (@hla){
						$hla=~s/\*//;
						my $seq=substr($seq_mut,$j,$i);
						print OUT3"$gene_name{$enst_id}\_$wild_aa$pos$mut_aa\_$pos1,$hla,$seq\n" if (length($seq)>=8);
					}			
				$pos1--;
				}
			}
		}else{
			$seq_left=substr($seq{$enst_id},0,$pos-1);
			$seq=$seq_left.$wild_aa.$seq_right;
			$seq_mut=$seq_left.$mut_aa.$seq_right;
			for my $i (8,9,10,11){
				my $start=0;
				$start=$pos-$i if ($pos>=$i);
				my $pos1=$pos-$start;
				for my $j ($start..$pos-1){
					foreach my $hla (@hla){
						$hla=~s/\*//;
						my $seq=substr($seq_mut,$j,$i);
						print OUT3"$gene_name{$enst_id}\_$wild_aa$pos$mut_aa\_$pos1,$hla,$seq\n"  if (length($seq)>=8);
					}			
				$pos1--;
				}
			}
		}
	}
	
	elsif ($mutation_type=~/inframe_deletion/){
		my @mutation=split /\//,$record[$pos_mut];
		$wild_aa=$mutation[0];
		my @pos=split/-/,$record[$position];
		$left_pos=$pos[0];
		$right_pos=$pos[1];
		$mut_aa=$mutation[1];
		next, if(!$seq{$enst_id} || !$gene_name{$enst_id});
		my ($id,$seq,$seq_mut,$seq_left,$seq_right);
		$seq_right=substr($seq{$enst_id},$right_pos,10);
		if($left_pos>=11){
			$seq_left=substr($seq{$enst_id},$left_pos-11,10);
			$seq=$seq_left.$wild_aa.$seq_right;
			$seq_mut=$seq_left.$mut_aa.$seq_right;
			$seq_mut=~s/\*//;
			for my $i (8,9,10,11){
				my $pos1=$i;
				for my $j (11-$i..10){
					foreach my $hla (@hla){
						$hla=~s/\*//;
						my $seq=substr($seq_mut,$j,$i);
						print OUT3"$gene_name{$enst_id}\_$wild_aa$left_pos\-$right_pos$mut_aa\_$pos1,$hla,$seq\n" if (length($seq)>=8);
					}			
				$pos1--;
				}
			}
		}else{
			$seq_left=substr($seq{$enst_id},0,$left_pos-1);
			$seq=$seq_left.$wild_aa.$seq_right;
			$seq_mut=$seq_left.$mut_aa.$seq_right;
			for my $i (8,9,10,11){
				my $start=0;
				$start=$pos-$i if ($pos>=$i);
				my $pos1=$pos-$start;
				for my $j ($start..$pos-1){
					foreach my $hla (@hla){
						$hla=~s/\*//;
						my $seq=substr($seq_mut,$j,$i);
						print OUT3"$gene_name{$enst_id}\_$wild_aa$pos$mut_aa\_$pos1,$hla,$seq\n"  if (length($seq)>=8);
					}			
				$pos1--;
				}
			}
		}
	}
	next, if(!$topology{$enst_id});
	
	my @outmembrane=split /-/, $topology{$enst_id};
	if ($mutation_type=~/missense_variant/){
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
		print OUT1 "$record\n", if($match_out==1);
		print OUT2 "$record\n", if($match_aa_char==1);
	}elsif($mutation_type=~/inframe_deletion/){
				foreach my $outmembrane(@outmembrane){
			if($outmembrane=~/^o(\d+)/){
				if($right_pos<$1){
					$match_out=1;
					if($aa_char{$wild_aa} ne $aa_char{$mut_aa}){
						$match_aa_char=1;
					}
				}
			}elsif($outmembrane=~/(\d+)o(\d+)/){
				if($left_pos>$1 && $right_pos<$2){
					$match_out=1;
					if($aa_char{$wild_aa} ne $aa_char{$mut_aa}){
						$match_aa_char=1;
					}
				}
			}elsif($outmembrane=~/(\d+)o$/){
				if($left_pos>$1){
					$match_out=1;
					if($aa_char{$wild_aa} ne $aa_char{$mut_aa}){
						$match_aa_char=1;
					}
				}
			}
		}
		print OUT1 "$record\n", if($match_out==1);
		print OUT2 "$record\n", if($match_aa_char==1);
	}
}

exit;
