# Shebang line here
#!/usr/bin/env python3
import argparse
import sys
import re
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--file_name", help="Input file name")
parser.add_argument("-f", "--FOLD", default=70, help="Ithe line fole,defalut is 70")
args = parser.parse_args()
file_name=args.file_name
FOLD=args.FOLD
def type_of_file(file_name):
    with open(file_name,'r') as f:
        f=f.readlines()
        for i in f:
            if re.search('#MEGA',i):
                mega(file_name)
            elif re.search('@.+',i):
                fastq(file_name)
            elif re.search('LOCUS\s',i):
                gb(file_name)
            elif re.search('ID\s',i):
                embl(file_name)

        
def fastq(file_name):
    seq=''
    s=''
    l=''
    with open(file_name,'r') as f:
        f=f.readlines()
        #print(f)
        for i in range(len(f)):
            f[i]=f[i].strip('\n')
            #print(f[3])
            search=re.match('@.+',f[i])
            search_else1=re.match('\+',f[i])
            search_else2=re.match('.*\?.+',f[i])
            if search:
                s+='\n'+f[i]+'\n'
            elif search_else1:
                l+=f[i]
            elif search_else2:
                l+=f[i]
            else:
                s+=f[i]
                seq+=f[i]
        st=extensiontype(seq)
        p=s.split("\n")[1:]
        #print(p)

        with open(writeextension(st), 'w') as out:
            for r in range(len(p)):
                search1=re.search('@.+',p[r])
                if search1:
                    if r>0:
                        out.write('\n'+'>'+p[r][1:]+'\n')
                    else:
                        out.write('>'+p[r][1:]+'\n')
                else:
                    for k in range(0, len(p[r]), int(FOLD)):
                        out.write(p[r][k:k+int(FOLD)])
def embl(file_name):
    seq=''
    title=''
    dna_or_aa=''
    with open(file_name,'r') as f:
        f=f.readlines()
        for i in f:
            if re.search('SQ',i):
                index_1=f.index(i)
            if re.search('//',i):
                index_2=f.index(i)
            if re.search('AC\s+',i):
                i=i.replace(re.search('AC\s+',i).group(),'>')
                title+=i
                title=title.replace(';','|')
                title=title.strip('\n')
            if re.search('DE\s+',i):
                i=i.replace(re.search('DE\s+',i).group(),'')
                i=i.strip('\n')
                title+=i
        #print(title)
        f=f[index_1+1:index_2]
        for x in f:
            if re.search('\s[0-9]+',x):
                x=x.replace(re.search('\s[0-9]+',x).group(),'')
            if re.search('\s',x):
                x=x.replace(re.search('\s',x).group(),'')
            x=x.strip('\n')
            seq+=x
            seq=seq.upper()
        st=extensiontype(seq)
        with open(writeextension(st),'w') as out:
            out.write(title+'\n')
            start=0
            seq_length=len(seq)
            while seq_length-start>=int(FOLD):
                out.write(seq[start:start+int(FOLD)]+'\n')
                start+=int(FOLD)
            while seq_length-start<=int(FOLD):
                out.write(seq[start:start+int(FOLD)])
                break
def mega(file_name):
    seq=''
    s=''
    with open(file_name,'r') as f:
        f=f.readlines()
        f=f[3:]
        for i in range(len(f)):
            f[i]=f[i].strip('\n')
            search=re.search('#.+',f[i])
            if search:
                s+='\n'+f[i]+'\n'
            else:
                s+=f[i]
                seq+=f[i]
        st=extensiontype(seq)
        #print(st)
        p=s.split("\n")[1:]
        with open(writeextension(st), 'w') as out:
            for r in range(len(p)):
                search1=re.search('#.+',p[r])
                if search1:
                    if r>0:
                        out.write('\n'+'>'+p[r][1:]+'\n')
                    else:
                        out.write('>'+p[r][1:]+'\n')
                else:
                    for k in range(0, len(p[r]), int(FOLD)):
                        out.write(p[r][k:k+int(FOLD)]+'\n')
def gb(file_name):
    seq=''
    title_ACCESSION=''
    title_DEFINITION=''
 
    dna_or_aa=''
    with open(file_name,'r') as f:
        f=f.readlines()
        for i in f:
            if re.search('ORIGIN',i):
                index_1A=f.index(i)
            if re.search('//',i):
                index_2A=f.index(i)
            if re.search('VERSION\s+',i):
                i=i.replace(re.search('VERSION\s+',i).group(),'>')
                title_ACCESSION+=i
                title_ACCESSION=title_ACCESSION.strip('\n')
            if re.search('DEFINITION\s+',i):
                i=i.replace(re.search('DEFINITION\s+',i).group(),' ')
                i=i.strip('\n')
                title_DEFINITION+=i
        title="{0}{1}" .format(title_ACCESSION, title_DEFINITION)
        f=f[index_1A+1:index_2A]
        for x in f:
            if re.search('\s[0-9]+',x):
                x=x.replace(re.search('\s[0-9]+',x).group(),'')
            if re.search('\s',x):
                x=x.replace(re.search('\s',x).group(),'')
            x=x.strip('\n')
            seq+=x
            seq=seq.upper()
        #print(seq)
        st=extensiontype(seq)
        with open(writeextension(st),'w') as out:
            out.write(title+'\n')
            start=0
            seq_length=len(seq)
            while seq_length-start>=int(FOLD):
                out.write(seq[start:start+int(FOLD)]+'\n')
                start+=int(FOLD)
            while seq_length-start<=int(FOLD):
                out.write(seq[start:start+int(FOLD)])
                break
def extensiontype(seq):
    dna_or_aa=''
    if re.search('[ACGTNacgtn]*',seq):
        dna_or_aa+='dna'
    else:
        dna_or_aa+='aa'
    return dna_or_aa
def writeextension(st):
    if '.' in file_name:
        sep='.'
        name = file_name.split(sep, 1)[0]
        if st=='dna':
            output_file=name+'.fna'
        elif st=='aa':
            output_file=name+'.faa'
        return output_file

def main():
    type_of_file(file_name)
                
if __name__ == '__main__':
    main()

# Your code here
