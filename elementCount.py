#!/usr/bin/env python3
import argparse
import sys
import re
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--file_name", help="Input file name")
args = parser.parse_args()
file_name=args.file_name
ch='chr1'
a=[]
c=[]
with open(file_name,'r') as f:
    for line in f:
        line=line.rstrip()
        line = line.split('\t')
        chromesome=line[0]
        intron_strat=line[1]
        intron_end=line[2]
        if chromesome==ch:
            location=(int(intron_strat),int(intron_end))
            a.extend(location)
            a=sorted(list(dict.fromkeys(a)))
            b=(int(intron_strat), int(intron_end))
            c.append(b)
        else:
            dic=[]
            for i in range(len(a)-1):
                h=[a[i],a[i+1],0]
                dic.append(h)
            for n in range(len(c)):
                start=a.index(c[n][0])
                end=a.index(c[n][1])
                for x in range(start,end):
                    dic[x][2]+=1
            for l in range(len(dic)):
                if dic[l][2] !=0:
                    print('{}\t{}\t{}\t{}'.format(ch,dic[l][0],dic[l][1],dic[l][2]))
                    
            ch=chromesome
            a=[]
            location=(int(intron_strat),int(intron_end))
            a.extend(location)
            b=()
            c=[]
            b=(int(intron_strat), int(intron_end))
            c.append(b)
            continue
    dic=[]
    for i in range(len(a)-1):
        h=[a[i],a[i+1],0]
        dic.append(h)
    for n in range(len(c)):
        start=a.index(c[n][0])
        end=a.index(c[n][1])
        for x in range(start,end):
            dic[x][2]+=1
    for l in range(len(dic)):
        if dic[l][2] !=0:
            print('{}\t{}\t{}\t{}'.format(ch,dic[l][0],dic[l][1],dic[l][2]))


         

                    
