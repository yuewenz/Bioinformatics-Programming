#/usr/bin/env python3
import sys;
def main():
    file_name1=sys.argv[1]
    file_name2=sys.argv[2]
    file_name3=sys.argv[3]
    text_file=open("output.txt", "w")
    know_file=open(file_name1 ,'r')
    ref_file= open(file_name2 ,'r')
    gene_file= open(file_name3 ,'r')
    gene_all=gene_file.read()[17:]
    gene_txt_all=",".join(gene_all.split())
    gene_txt=gene_txt_all.split(',')
    output1 = open('file1.txt','w')
    dic={}
    uscsid={}
    new_dic={}
    result={}
    res={}
    for line in ref_file:
        #L=[]
        line = line.split('\t')
       # L.extend(([line[0]],line[4]))
        if line[4] in gene_txt:
            new_dic[line[0]]=line[4]
            for key,value in new_dic.items():
                if value not in uscsid.values():
                    uscsid[key]=value
                    inv_uscsid = {v: k for k, v in uscsid.items()}
    #text_file.write(str(inv_uscsid))
    #print(len(list(uscsid.values())))
    for know_line in know_file:
        know_line=know_line.split('\t')
        x=[]
        z=[]
        #c=[]
        #x.extend(([know_line[0]],know_line[1],know_line[3],know_line[4]))
        if know_line[0] in list(uscsid.keys()):
            z.extend((know_line[1],know_line[3],know_line[4]))
            result[know_line[0]]= z
    #text_file.write(str(result))
    for key, value in inv_uscsid.items():
        for keyy, valuee in result.items():
            if value==keyy:
                res[key]=valuee
    #res.insert_before('PIK3CD',{'Gene':['Chr','Stop','Start']})
    y=''
    for key in sorted(res.keys()):
        a="%s\t%s" %(key, res[key][0])
        b="%s\t%s" %(a,res[key][1])
        c="%s\t%s" %(b,res[key][2])
        y+='\n'+c
    print('Gene\tChr\tStart\tStop'+y)
    #print("{}".format("Gene\tChr\tStart\tStop\n")+c)
        #d="Gene\tChr\tStart\tStop\n"+c
        #print(d)
if ( __name__ == "__main__" ):
    main();
    
# Write your code here.  Print your output to standard out.


