#!/bin/bash

# Place your gatech userame in the below export
export NAME="yuewenz"

get_input () {
	# Function for doing your getopts
	#
	# Input: Getopts array
	while getopts "a:b:r:eo:f:zvih" option
	do
		case $option in
			a) reads1=$OPTARG;;
			b) reads2=$OPTARG;;
			r) ref=$OPTARG;;
			e) realign=1
			echo "preformace read realign file"
			;;
			o) output=$OPTARG;;
			f) millsFile=$OPTARG;;
			z) gunzip=1
			echo "Output VCF file should be gunzipped (*.vcf.gz)"
			;;
			v) v=1
			echo "Verbose mode"
			;;
			i) index=1
			echo "Index your output BAM"
			;;
			h) echo "Usage information"
			exit 0
			;;
	esac
done




	# Replace
	# this
	# with
	# getopts
	# code
}

check_files () {
	# Function for checking for presence of input files, reference genome,
	# and the output VCF file
	#
	#reads1="./reads1.fq" 
	if [ -e "$reads1" ]
	then
		echo "True"
	else
		echo "reads1.fq is missing"
		exit 1
	fi
	if [ -e "$reads2" ]
        then
                echo "True"
        else
                echo "reads2.fq is missing"
		exit 1
        fi
	if [ -e "$ref" ]
	then
		echo "True"
	else
		echo "ref.fa is missing"
		exit 1
	fi
	if [ -e "$millsFile" ]
	then
		echo "True"
	else 
		echo "millsFile is missing"
		exit 1
	fi
	if [ -e "$output" ]
	then
		read -r -p "The $output alreay exist, what should you want to do? Overwrite or non-overwrite" answer
		if [[ "$answer" =~ Overwrite ]]
		then
			rm $output
		else
			echo "It is good to go"
		fi
	else
		echo "There are no exist file or program"
	fi
	# Input: File locations (string)
	# Output: True, if checks pass; False, if checks fail (bool)

	# Replace
	# this
	# with
	# code
}

prepare_temp () {
	# Preparing your temporary directory
	#
	# 
	tmp="$1"
	if [ -d "tmp" ]
	then
		echo "$tmp exist!"
	else
		mkdir tmp
	fi

	# Replace
	# this
	# with
	# getopts
	# code
}


mapping () {
	# Function for the mapping step of the SNP-calling pipeline
	#
	# Input: File locations (string), Verbose flag (bool)
	# Output: File locations (string)
	if [[ $v -eq 1 ]]
	then
		echo "This is for mapping and gain the lane_sorted.bam file for follwing step."
	fi
	#ref="./ref.fa"
	#reads1="./reads1.fq"
	#reads2="./reads2.fq"
	samtools faidx "$ref"
	bwa index "$ref"
	bwa mem -R '@RG\tID:foo\tSM:bar\tLB:library1' "$ref" "$reads1" "$reads2" > lane.sam
	samtools fixmate -O bam lane.sam lane_fixmate.bam
	samtools sort -O bam -o lane_sorted.bam -T ./tmp/lane_temp lane_fixmate.bam


	# Replace
	# this
	# with
	# code
}

improvement () {
	# Function for improving the number of miscalls
	#
	# Input: File locations (string)
	# Output: File locations (string)
	if [[ $v -eq 1 ]]
	then
		echo "This is improvement. This is for reducing the number of miscalls of INDELs in your data it is helpful to realign your raw gapped alignment with the Broad’s GATK Realigner."
	fi
	java -jar ./lib/picard.jar CreateSequenceDictionary R=$ref O=ref.dict
	#ref="./ref.fa"
	#millsFiles="./Mills_and_1000G_gold_standard.indels.hg38.vcf"
	if [[ "$index" -eq 1 ]]
	then
		samtools index lane_sorted.bam
	fi
	java -Xmx2g -jar ./lib/GenomeAnalysisTK.jar -T RealignerTargetCreator -R "$ref" -I lane_sorted.bam -o lane.intervals --known "$millsFile" &> ./output/yuewenz.log
	if [[ "$realign" -eq 1 ]]
	then
		java -Xmx4g -jar ./lib/GenomeAnalysisTK.jar -T IndelRealigner -R "$ref" -I lane_sorted.bam -targetIntervals lane.intervals -known "$millsFile" -o lane_realigned.bam &>> ./output/yuewenz.log
		if [[ "$index" -eq 1 ]]
        	then
                	samtools index lane_realigned.bam
		fi
	fi

	#fi
	# Replace
	# this
	# with
	# code
}

call_variants () {
	# Function to call variants
	#
	# Input: File locations (string)
	# Ouput: None
	#ref="./ref.fa"
	#output="yuewenz.vcf.gz"
	if [ -e "$realign" ]
	then
		bcftools mpileup -Ou -f "$ref" lane_realigned.bam | bcftools call -vmO z -o ./output/"$output".vcf.gz
	else
		bcftools mpileup -Ou -f "$ref" lane_sorted.bam | bcftools call -vmO z -o ./output/"$output".vcf.gz
	fi

	# Replace
	# this
	# with
	#code
}


gun_zip () {
	#output="yuewenz.vcf.gz"
	if [[ "$gunzip" -eq 1 ]]
	then
        	gunzip -c output/"$output".vcf.gz > ./output/yuewenz.vcf
	else
		output/"$output".vcf.gz
	fi



	# Replace
	# this
	# with
	#cod
}

convert () {
	if [[ "$gunzip" -eq 1 ]]
	then
	       	grep -o '^[^#]*' ./output/yuewenz.vcf | awk '{gsub(/^chr/,""); print}' | cut -f1-5 | awk -v FS="\t" -v OFS="\t" '{ print $1, $2, $2+(length($5)-length($4)), length($5)-length($4); }' | awk '{if ($4!= 0) print >"./output/indels.txt"; else print >"./output/snps.txt"}'
	else
		gunzip -c ./output/"$output".vcf.gz | grep -o '^[^#]*' | awk '{gsub(/^chr/,""); print}' | cut -f1-5 | awk -v FS="\t" -v OFS="\t" '{ print $1, $2, $2+(length($5)-length($4)), length($5)-length($4); }' | awk '{if ($4!= 0) print >"./output/indels.txt"; else print >"./output/snps.txt"}'
	fi
}

main() {
	# Function that defines the order in which functions will be called
	# You will see this construct and convention in a lot of structured code.
	
	# Add flow control as you see appropriate
	get_input "$@"
	check_files # Add arguments here
	prepare_temp
	mapping # Add arguments here
	improvement # Add arguments here
	call_variants # Add arguments here
	gun_zip
	convert
}

# Calling the main function
main "$@"


# DO NOT EDIT THE BELOW FUNCTION
bats_test (){
    command -v bats
}
# DO NOT EDIT THE ABOVE FUNCTION
