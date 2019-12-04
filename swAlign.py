#!/usr/bin/env python3
import sys
def main():
    file_name1=sys.argv[1]#rows
    file_name2=sys.argv[2]#cols
    #score calculate
    match = 1
    gap = -1
    mismatch = -1
    # making matrix
    alignment=[]
    with open(file_name1 ,'r') as rows_file:
        content=rows_file.readlines()
        content=content[1:]
        for line_row in content:
            line_row=line_row.strip()
    with open(file_name2 ,'r') as cols_file:
        content_r=cols_file.readlines()
        content_r=content_r[1:]
        for line_cols in content_r:
            line_cols=line_cols.strip()
    for i in range(len(line_row)+1):
        temp=[]
        for x in range(len(line_cols)+1):
            temp.append(0)
        alignment.append(temp)
    #print(alignment)
    #add to first row
    for l in range(len(line_cols)+1):
        alignment[0][l]=gap*l
        if alignment[0][l]<0:
            alignment[0][l]=0
    #add to first col
    for p in range(len(line_row)+1):
        alignment[p][0]=gap*p
        if alignment[p][0]<0:
            alignment[p][0]=0
    #add to other place:
    for x in range(1,len(line_row)+1):
        for y in range(1,len(line_cols)+1):
            score1=alignment[x-1][y]+gap
            if score1<0:
                score1=0
            score2=alignment[x][y-1]+gap
            if score2<0:
                score2=0
            if line_cols[y-1]==line_row[x-1]:
                score3=alignment[x-1][y-1]+match
                if score3<0:
                    score3=0
            elif line_cols[y-1] != line_row[x-1]:
                score3=alignment[x-1][y-1]+mismatch
                if score3<0:
                    score3=0
            alignment[x][y]=max(score1,score2,score3)
    #print(alignment)
    dup = []
    for ksample in alignment:
        for isample in ksample:
            dup.append(isample)
            max_item=max(dup)
    #print(max_item)
    for index, row in enumerate(alignment):
        if max_item in row:
            m=index
            n=row.index(max_item)
    #print(m,n)
    a_1=[]
    a_2=[]
    alinment_score=0
    while n>0 and m>0:
        current_base=alignment[m][n]
        #print(current_base)
        diag_base=alignment[m-1][n-1]
        #print(diag_base)
        top_base=alignment[m-1][n]
        left_base=alignment[m][n-1]
        if current_base !=0:
            if current_base !=top_base+gap:
                if current_base!=left_base+gap:
                    if current_base == diag_base + match:
                        a_2+=line_cols[n-1]
                        a_1+=line_row[m-1]
                        m-=1
                        n-=1
                        alinment_score+=match
                        #print(a_1)
                    elif current_base == diag_base + mismatch:
                        a_2+=line_cols[n-1]
                        a_1+=line_row[m-1]
                        m-=1
                        n-=1
                        alinment_score+=mismatch
                        #print(a_1)
                #print(current_base)

                elif current_base==left_base+gap:
                    a_1+='-'
                    a_2+=line_cols[n-1]
                    n-=1
                    alinment_score+=gap

            else:
                a_1+=line_row[m-1]
                a_2+='-'
                m-=1
                alinment_score+=gap
        else:
            break

    a_1=a_1[::-1]
    a_2=a_2[::-1]
    a_1_str=''
    a_2_str=''
    matchlines=''
    y=0
    for item in a_1:
        a_1_str+=item
    for items in a_2:
        a_2_str+=items
    for k in a_1_str:
        if k == a_2_str[y]:
            matchlines+="|"
        else:
            if k =='-':
                matchlines+=' '
            elif a_2_str[y] == '-':
                matchlines+=' '
            else:
                matchlines+='*'
        y+=1
    print(a_1_str+'\n'+matchlines+'\n'+a_2_str+'\n'+"Alignment score: "+str(alinment_score)) 
          

if ( __name__ == "__main__" ):
    main();

# Write your code here
