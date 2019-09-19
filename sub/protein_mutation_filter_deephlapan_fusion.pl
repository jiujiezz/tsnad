#!/usr/bin/perl-w
#use strict;

my $in=$ARGV[0];;
my $out=$ARGV[1];;
my $hla=$ARGV[2];

open IN, "<$in" or die "Can not open file $in:$!";
open OUT, ">$out" or die "Can not open file $out:$!";
open HLA, "<$hla" or die "Can not open file $hla:$!";

print OUT"Annotation,HLA,peptide\n";

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

my @head=split/\t/,<IN>;
my %mark;
my $sequence;
my $annotate;
while (<IN>){
	chomp;
	my @line=split/\t/,$_;
	if ($line[-2]!~/\./){
		my @seq=split/\|/,$line[-2];
		$seq[1]=~s/\*//g;
		$line[1]=~s/\(.*\)//g;
		$annotate=$line[0]."_".$line[1];
		if ($seq[0]!~/\*/){
			my $seq_before=substr($seq[0],length($seq[0])-10,10);
			$sequence=$seq_before.$seq[1];
			$sequence=uc($sequence);
		}
		elsif ($seq[0]=~/\*/){
			my @lines=split/\*/,$seq[0];
			if ($lines[0]=~/[a-z]/){
				$sequence=uc($lines[0]);
			}
		}
		for my $i (8,9,10,11){
			for my $j (11-$i..10){
				foreach my $hla (@hla){
					$hla=~s/\*//;
					my $seq=substr($sequence,$j,$i);
					print OUT"$annotate,$hla,$seq\n" if (length($seq)>=8);
				}
			}
		}
	}
}