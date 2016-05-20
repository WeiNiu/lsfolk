from __future__ import division
import cjson
from operator import itemgetter
from collections import defaultdict
infile='./link-dict_en_lt10_3'
#infile='./link-dict_ny_u5_10'
infile=open(infile,'r')

#outfile='link-2'
#out=open(outfile,'w')
tagdict=cjson.decode(infile.readline())
#tagdict1=defaultdict(dict)
tagfreq={}
count=0
for key,value in tagdict.iteritems():
    freq=tagdict[key][key]
    count+=1
    print count
    for key1,value1 in value.iteritems():
        if tagdict[key][key1]>=3:
            tagdict[key][key1]=tagdict[key][key1]/freq
        else:
            tagdict[key][key1]=0
#outfile1='probs'
#out1=open(outfile1,'w')
#for key,value in tagdict.iteritems():
#    print>> out1, [key,value]
print'_______1_______'
rulelist=[]
outfile2='rulelist_en_new_lt10_2_part1'
outfile2='rulelist_lt10_schz_test'
out2=open(outfile2,'w')
for key,value in tagdict.iteritems():
    for key1,value1 in value.iteritems():
        if value1>0.6:
            a=tagdict[key1][key]
            if a<0.6 and a!=0:    
                rulelist.append([key1,key,value1,a])
        #if value1>0.3:
        #    a=tagdict[key1][key]
        #    if a>0.1:    
        #        rulelist.append([key1,key,value1,a])

rules=sorted(rulelist,key=itemgetter(2),reverse=True)
for rule in rules:
    out2.write(cjson.encode(rule)+'\n')
