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
MAXF=150668#news version2
MAXF=28097.7#news chicago
MAXF=20703.6#chicago
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
    if common>=3 and freq1>=freq2:
        weight=(1-(log(freq1)-log(freq2))/lMAXF)
        #print weight
        #weight=(1-(freq1-freq2)/MAXF)

        relation[key1][key2]=common/freq2*weight
    elif common>=3 and freq2>=freq1:
        weight=(1-(log(freq2)-log(freq1))/lMAXF)
        #weight=(1-(freq2-freq1)/MAXF)
        #print weight
        relation[key2][key1]=common/freq1*weight

print'_______1_______'
rulelist=[]
outfile2='/spare/wei/local/rulelist_en_ch3-log'

out2=open(outfile2,'w')
for key,value in relation.iteritems():
    for key1,value1 in value.iteritems():
        if value1>0.0000001 and value1!=1 and key!=key1:
            rulelist.append([key1,key,value1])
rules=sorted(rulelist,key=itemgetter(2),reverse=True)
for rule in rules:
    out2.write(cjson.encode(rule)+'\n')
