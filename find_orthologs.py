#!/usr/bin/env python3

'''
Script for finding orthologs using reciprocal BLAST hits.

You may choose to import any of the other allowed modules.

You have to write an argparse for getting command line arguments. The usage for
this script is:
    ./find_orthologs.py -i1 <Input file 1> -i2 <Input file 2> -o <Output file name> –t <Sequence type – n/p>

where "n" specifies a nucleotide sequence and "p" specifies a protein sequence.
'''
#blastp -query mc58.fasta -db fam18.fasta -outfmt 6
#makeblastdb -in fam18.fasta -dbtype prot
import argparse
import os
import subprocess
def main():
    '''
    This is the main function.
    '''
    
    '''
    Insert argparse code that populates the following variables
     - file_one
     - file_two
     - output_file
     - input_sequence_type
    '''
    # Argparse code
    parser = argparse.ArgumentParser()
    parser.add_argument("-i1", "--file_one", help="Input file 1")
    parser.add_argument("-i2", "--file_two", help="Input file 2")
    parser.add_argument("-o", "--output_file", help="Output file name")
    parser.add_argument("-t", "--input_sequence_type", help="Sequence type – n/p")
    args = parser.parse_args()
    #if args.file_one:
        #file_one=open(args.file_one,'r')
    #if args.file_two:
        #file_two=open(args.file_two,'r')
    file_one= args.file_one
    file_two=args.file_two
    input_sequence_type=args.input_sequence_type
    output_file= args.output_file

    def get_reciprocal_hits(file_one, file_two, input_sequence_type):
        if input_sequence_type == 'p':
            database1=subprocess.call(['makeblastdb','-in',file_one,'-dbtype', 'prot','-out','database1'])
            database2=subprocess.call(['makeblastdb','-in',file_two,'-dbtype', 'prot','-out','database2'])
        elif input_sequence_type == 'n':
            database1=subprocess.call(['makeblastdb','-in',file_one,'-dbtype', 'nucl','-out','database1'])
            database2=subprocess.call(['makeblastdb','-in',file_two,'-dbtype', 'nucl','-out','database2'])
#blastp -query mc58.fasta -db fam18.fasta -outfmt 6
        #database1
        if input_sequence_type == 'p':
            blast1=subprocess.call(['blastp', '-query', file_two, '-db', 'database1', '-out', 'blast1.txt','-outfmt', '6'])
        elif input_sequence_type == 'n':
            blast1=subprocess.call(['blastn', '-query', file_two, '-db', 'database1', '-out', 'blast1.txt','-outfmt', '6'])
        #database2
        if input_sequence_type == 'p':
            blast2=subprocess.call(['blastp', '-query', file_one, '-db', 'database2', '-out', 'blast2.txt','-outfmt', '6'])
        elif input_sequence_type == 'n':
            blast2=subprocess.call(['blastn', '-query', file_one, '-db', 'database2', '-out', 'blast2.txt','-outfmt', '6'])
            
        #datacompare
        d1 ={}
        with open('blast1.txt', 'r') as fl1:
            for line in fl1:
                line.strip()
                elements = line.split('\t')
                queryID=elements[0]
                subjectID=elements[1]
                if queryID not in d1.keys():
                    d1[queryID]=subjectID
        d2 ={}
        with open('blast2.txt', 'r') as fl2:
            for line in fl2:
                line.strip()
                elements = line.split('\t')
                queryID=elements[0]
                subjectID=elements[1]
                if queryID not in d2.keys():
                    d2[queryID]=subjectID
        same={}
        for dict1 in d1.keys():
            value1=d1[dict1]
            if value1 in d2.keys():
                if dict1 == d2[value1]:
                    same[dict1] = value1
        dictlist=[]
        for key in same.keys():
            dictlist+=["%s\t%s\n" %(key, same[key])]

        
        return dictlist
        



    '''
    output_list is a list of reciprocal BLAST hits. Each element is a tab
    separated pair of gene names. Eg:
    ["lcl|AM421808.1_cds_CAM09336.1_10	lcl|AE002098.2_cds_NMB0033_33", "lcl|AM421808.1_cds_CAM09337.1_11	lcl|AE002098.2_cds_NMB0034_34", "lcl|AM421808.1_cds_CAM09338.1_12	lcl|AE002098.2_cds_NMB0035_35", "lcl|AM421808.1_cds_CAM09339.1_13	lcl|AE002098.2_cds_NMB0036_36", ...]
    '''
    output_list = get_reciprocal_hits(file_one, file_two, input_sequence_type)
    with open(output_file, 'w') as output_fh:
        for ortholog_pair in output_list:
            output_fh.write(ortholog_pair)
      #REMOVE      
    location =  os.getcwd()
    filenames = os.listdir(location)
    for file in filenames:
        if 'database1' in file:
            path = os.path.join(location, file)
            os.remove(path)
        elif 'database2' in file:
            path = os.path.join(location, file)
            os.remove(path)
        elif 'blast1.txt' in file:
            path = os.path.join(location, file)
            os.remove(path)
        elif 'blast2.txt' in file:
            path = os.path.join(location, file)
            os.remove(path)

if __name__ == "__main__":
    main()
