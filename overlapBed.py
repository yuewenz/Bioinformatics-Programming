#!/usr/bin/env python
import argparse
#TAKING IN THE INPUT FROM USER
parser=argparse.ArgumentParser('Overlap Regions')
parser.add_argument('-i1','--file1')
parser.add_argument('-i2','--file2')
parser.add_argument('-m','--cutoff')
parser.add_argument('-o','--output')
parser.add_argument('-j','--jflag',action='store_true')
args=parser.parse_args()
file1=args.file1
file2=args.file2
min_overlap=int(args.cutoff)
output_file=args.output
j=args.jflag

#INITIALIZING VARIABLES
te={}
intron={}
intron_line={}
te_line={}
intron_index=0
overlap_start_te=0
chromosome_list=[]

#READING IN FILES
with open(file1,'r') as f1:
    with open(file2,'r') as f2:
        #READ IN THE INTRON FILE
        for line1 in f1:
            line1=line1.strip()
            if (line1.split()[0] not in intron):
                intron[line1.split()[0]]=[]
                intron_line[line1.split()[0]]=[]
            if (line1.split()[0] in intron):
                intron[line1.split()[0]].append(line1.split())
                intron_line[line1.split()[0]].append(line1)

        #READ IN THE TE FILE
        for line2 in f2:
            line2=line2.strip()
            if (line2.split()[0] not in te):
                te[line2.split()[0]]=[]
                te_line[line2.split()[0]]=[]
            if (line2.split()[0] in te):
                te[line2.split()[0]].append(line2.split())
                te_line[line2.split()[0]].append(line2)
                
        #STORING THE CHROMOSOMES IN A LIST
        for i in intron:
            chromosome_list.append(i)
            
        #SETTING THE INITIAL TE INDEX
        for chromosome in chromosome_list:
            overlap_start_te=0
            for intron_index in range(len(intron[chromosome])):
                start_intron=int(intron[chromosome][intron_index][1])
                stop_intron=int(intron[chromosome][intron_index][2])
                set_start=False
                te_index=overlap_start_te
                while intron_index<len(intron[chromosome]):
                    #SETTING THE TE INDEX BACK TO POINT IT FOUND THE FIRST OVERLAP
                    if te_index>=len(te[chromosome]):
                        break
                    start_te=int(te[chromosome][te_index][1])
                    stop_te=int(te[chromosome][te_index][2])
                    overlap=min(stop_te,stop_intron)-max(start_te,start_intron)
                    if (stop_te<start_intron and set_start==False):
                        #TE is lagging behind, so moving TE forward
                        te_index+=1
                        continue
                    if (overlap>=0):
                        try:
                            overlap_perc=(overlap/(stop_intron-start_intron))*100
                        except:
                            overlap_perc=100
                            overlap=1
                        if (set_start==False):
                            overlap_start_te=te_index
                            set_start=True
                        ##CHECK IF THIS LINE CAUSES DUPLICATE OVERLAPS
                        if (set_start==True and overlap_perc<min_overlap):
                            te_index+=1
                            continue
                        if (set_start==True and overlap_perc>=min_overlap):
                            with open(output_file,'a+') as f:
                                if j==True:
                                    print(intron_line[chromosome][intron_index]+'\t'+te_line[chromosome][te_index],file=f)
                                if j==False:
                                    print(intron_line[chromosome][intron_index],file=f)
                                    break
                            te_index+=1
                            continue
                    if (start_te>stop_intron and set_start==True):
                        break
                    else:
                        break
