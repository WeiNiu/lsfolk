from __future__ import division
import cjson
from operator import itemgetter
from collections import defaultdict
from math import log
infile='/spare/wei/local/tag-tag-dict_ch3'
#infile='./link-dict_ny_u5_10'
infile=open(infile,'r')
tag_freq_dict='/spare/wei/local/tag_freq_dict_ch3'
infile1=open(tag_freq_dict,'r')
tagdict=cjson.decode(infile.readline())
tag_freq_dict=cjson.decode(infile1.readline())
#tagdict1=defaultdict(dict)
#tagfreq={}
#for key,value in tag_user_dict.iteritems():
#    tagfreq[key]=value[-1]
count=0
MAXF=578056 #news
MAXF=28097.7
MAXF=20723.6
lMAXF=log(MAXF)
relation=defaultdict(dict)
for key,value in tagdict.iteritems():
    key=key.split('_')
    key1,key2=key[0],key[1]
    #freq1=tagdict[key1+'_'+key1]
    #freq2=tagdict[key2+'_'+key2]
    freq1=tag_freq_dict[key1]
    freq2=tag_freq_dict[key2]
    common=tagdict.get(key1+'_'+key2,tagdict.get(key2+'_'+key1))
    if common>=3:
        weight=(1-abs(log(freq1)-log(freq2))/lMAXF)
        #print weight
        #weight=(1-abs(freq1-freq2)/MAXF)

        relation[key1][key2]=common/freq2*weight
    
        #weight=(1-(log(freq2)-log(freq1))/lMAXF)
        #weight=(1-(freq2-freq1)/MAXF)
        #print weight
        relation[key2][key1]=common/freq1*weight

print'_______1_______'
rulelist=[]
outfile2='/spare/wei/local/chi_rulelist_en_0.1_bidirectioni_log'

out2=open(outfile2,'w')
for key,value in relation.iteritems():
    for key1,value1 in value.iteritems():
        if value1>0.1 and value1!=1 and key!=key1:
            rulelist.append([key1,key,value1])
rules=sorted(rulelist,key=itemgetter(2),reverse=True)
for rule in rules:
    out2.write(cjson.encode(rule)+'\n')
