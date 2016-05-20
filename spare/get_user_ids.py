#get user ids for timeline crawling. these users are mostly listed
import cjson
infile='./user_tag_dict_sift'
outfile='./uids'
outfile=open(outfile,'w')
for line in open(infile,'r'):
    line=line.split('\t')[0]
    outfile.write(line+'\n')

