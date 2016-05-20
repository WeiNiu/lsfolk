#build conditional probability according to tag_multi_prime
import cjson
import sys
infile=sys.argv[1]
outfile=sys.argv[2]
condition_p={}
for line in open(infile,'r'):
    line=cjson.decode(line)
    key=line[0]+'_'+line[1]
    condition_p[key]=line[2]
outfile=open(outfile,'w')
outfile.write(cjson.encode(condition_p)+'\n')

