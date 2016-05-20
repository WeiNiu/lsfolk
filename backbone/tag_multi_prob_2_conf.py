from __future__ import division
import cjson
import sys
from operator import itemgetter
from collections import defaultdict
from math import log
dist1=[0 for i in range(101)]
dist2=[0 for i in range(101)]
infile=sys.argv[1]#'/spare/wei/local/tag-tag-dict_ch3'
#infile='./link-dict_ny_u5_10'
infile=open(infile,'r')
tag_freq_dict=sys.argv[2]#'/spare/wei/local/tag_freq_dict_ch3'
infile1=open(tag_freq_dict,'r')
tagdict=cjson.decode(infile.readline())
tag_freq_dict=cjson.decode(infile1.readline())
#tagdict1=defaultdict(dict)
#tagfreq={}
#for key,value in tag_user_dict.iteritems():
#    tagfreq[key]=value[-1]
MAX=sorted(tag_freq_dict.items(),key=itemgetter(1),reverse=1)[0]
print MAX
MAXF=MAX[1]
MAXF+=1
count=0
#MAXF=578056 #news
#MAXF=150668#news version2
#MAXF=28097.7#news chicago
#MAXF=20703.6#chicago
lMAXF=log(MAXF)
relation=defaultdict(dict)
removelist=[]
for key,value in tagdict.iteritems():
    key=key.split('_')
    key1,key2=key[0],key[1]
    #freq1=tagdict[key1+'_'+key1]
    #freq2=tagdict[key2+'_'+key2]
    freq1=tag_freq_dict[key1]
    freq2=tag_freq_dict[key2]
    common=tagdict.get(key1+'_'+key2,tagdict.get(key2+'_'+key1))
    if common>=3 and freq1>=freq2:
        #weight=(1-(log(freq1)-log(freq2))/lMAXF-(freq1-freq2)/(4*freq1))
        #print weight
        #weight=(1-(freq1-freq2)/(MAXF-freq2))
        weight=1#-log(freq1/freq2)/log(MAXF)#+0.5*(freq1-freq2)/(freq2+freq1))
        x1=common/freq2*weight
        x2=common/freq2
        #print key,key1, x2, weight
        #dist1[int(x1*100)]+=1
        #dist2[int(x2*100)]+=1
        relation[key1][key2]=[x1,x2,freq2]
        #if freq1/freq2<2 and x1>0.95 and key1!=key2 and ' ' not in key1:
        #    print 'remove first',key1,key2,x1,common,freq1,freq2
        #    removelist.append(key1)
        #elif x1==1  and key1!=key2 and ' ' in key1:
        #    print key1, key2,'test',freq1, freq2
        #    removelist.append(key2)
    elif common>=3 and freq2>freq1:
        #weight=(1-(log(freq2)-log(freq1))/lMAXF-(freq2-freq1)/(4*freq2))
        #weight=(1-(freq2-freq1)/(MAXF-freq1))
        #print weight
        weight=1#-log(freq2/freq1)/log(MAXF)#+0.5*(freq2-freq1)/(freq2+freq1))
        x1=common/freq1*weight
        x2=common/freq1
        #print key,key1,x2,weight
        #if freq2/freq1<2 and x1>0.95 and key1!=key2 and ' ' not in key2:
        #    print 'remove second',key1,key2,x1,common,freq1,freq2
        #    removelist.append(key2)
        #relation[key2][key1]=[x1,x2,freq1]
    #elif freq1 ==freq2 and common>=3:
    #    if ' ' in key1:
    #        removelist.append(key2)
    #    elif ' ' in key2:
    #        removelist.append(key1)
#print removelist    
#print'_______1_______'
rulelist=[]
outfile2=sys.argv[3]#'/spare/wei/local/rulelist_en_ch3-log'

out2=open(outfile2,'w')
for key,value in relation.iteritems():
    if key in removelist:
        print key
        continue
    for key1,value1 in value.iteritems():
        if key1 in removelist:
            continue
        if value1[0]>0.1 and key!=key1:
            if (key in key1 or key1 in key) and value1[0]==1:
                continue
            else:
                rulelist.append([key1,key,value1[0],value1[2]])
rules=sorted(rulelist,key=itemgetter(2),reverse=True)
for rule in rules:
    out2.write(cjson.encode(rule)+'\n')
#print dist1
#print dist2
removelistf=open(sys.argv[4],'w')
removelistf.write(cjson.encode(removelist))
