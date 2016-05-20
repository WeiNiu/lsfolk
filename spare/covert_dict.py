#build conditional probability according to tag_multi_prime
import cjson
infile='./local/chi_rulelist_en_0.1_bidirection_log'
outfile='./local/chi_condition_p_log'
condition_p={}
for line in open(infile,'r'):
    line=cjson.decode(line)
    key=line[0]+'_'+line[1]
    condition_p[key]=line[2]
outfile=open(outfile,'w')
outfile.write(cjson.encode(condition_p)+'\n')

