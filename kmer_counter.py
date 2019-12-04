#/usr/bin/env python3
import sys;
#print sys.argv[0] # prints python_script.py
#k= sys.argv[1] # prints var1
#file_name= sys.argv[2] # prints var2
#file_name = input ('name of the file')
#file_handler=open(file_name ,'r')
#all_text = file_handler.read()[71:]
#k_mer_text="".join(all_text.split())
#print(k_mer_text)
def main():
    file_name = sys.argv[2];
    k = int(sys.argv[1]);
    file_handler = open(file_name ,'r')
    all_text = file_handler.read()[71:]
    k_mer_text="".join(all_text.split())
    kmer_dict={}
    #text_file=open("q1-kmer.out.txt", "w")
    for i in range(len(k_mer_text)-k+1): #{
        kmer_number = k_mer_text[i:i+k]
        if kmer_number not in kmer_dict: #{
            kmer_dict[kmer_number]=1
        #}
        else: #{
            kmer_dict[kmer_number]+=1
        #}
    #}
    
    for key in sorted(kmer_dict.keys()): #{
        print("%s\t%s" %(key, kmer_dict[key]))
    #}
#}

if ( __name__ == "__main__" ): #{
    main();
#}
#k_merdict=k_mer_fre(k_mer_text,5)

#for key in sorted(k_mer_frequence.keys()):
    #print("%s\t%s" % (key, k_mer_frequence[key]))

# Write your code here.  Print your output to standard out.


