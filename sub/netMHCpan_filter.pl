# Finish time: January, 2016.
# Developer: Zhan Zhou, Xingzheng Lyu, Jingcheng Wu
# Copyright (C) 2015-2016 - College of Pharmaceutical Sciences, 
#               Zhejiang University - All Rights Reserved 
# *************************************************************
use strict;

my $in2=$ARGV[0]; #input netMHCpan output file
my $out1=$ARGV[1]; #output binding information

#open IN1, "<$in1" or die "Can not open file $in1:$!";
open IN2, "<$in2" or die "Can not open file $in2:$!";
open OUT1, ">$out1" or die "Can not open file $out1:$!";

print OUT1 "Position\tHLA\twild peptide\twild binding\twild rank\twild binding level\t<------------------->\tmutant peptide\tmutant binding\tmutant rank\tmutant binding level\n";
my @binding;
my $identity;
my @identity;

#print OUT1 "Position\tMHC\twild_Peptide\tID\t1-log50k(aff)\tAffinity(nM)\t%Rank\tBindLevel\taccordance\tPosition\tMHC\tmut_Peptide\tID\t1-log50k(aff)\tAffinity(nM)\t%Rank\tBindLevel\n";


my (%mark,%mark1);
my $line1;
while(<IN2>){
    chomp;
    my $line=$_;
    my $enst_id;
    $line=~s/<=//;
    my @line=split /\s+/, $line;
    shift @line;
    $line1=join "\t",@line;
    my $pos=$line[0];
    my $pep=$line[2];
    my $len_pep=length($pep);
    my @mut=split/_/,$line[10];
   # my $gene=$mut[0];	
	if ($mut[1]=~/([A-Z]+\d+$)/){
		$mark{$line[0]."\t".$line[1]."\t".$len_pep."\t".$line[10]}=join "\t", @line[0,1,2,12,13,14] if ($line[14]);
		$mark{$line[0]."\t".$line[1]."\t".$len_pep."\t".$line[10]}=join "\t", @line[0,1,2,12,13],'-' if (!$line[14]);
	}
    if($line[1]=~/HLA/ && ($line[14]=~/WB|SB/)){
        next, if($pos>11 || ($pos+$len_pep)<12);
		if ($mut[1]=~/([A-Z]+\d+)[A-Z]+/){
			my $aa=$1;
			$mark1{$line[0]."\t".$line[1]."\t".$len_pep."\t".$line[10]}=join "\t", @line[2,10,12,13,14];
		}
	}
}

foreach my $file (keys %mark1){
	my $pos;
	my @mut=split/\t/,$file;
	if ($mut[3]=~/^(.*[A-Z]+\d+)[A-Z]+/){
		$pos=$1;
	}
	my $id=$mut[0]."\t".$mut[1]."\t".$mut[2]."\t".$pos;
	print OUT1"$mark{$id}\t<------------------->\t$mark1{$file}\n";
}   

#close IN1;                      
close IN2;              
close OUT1;
exit;
