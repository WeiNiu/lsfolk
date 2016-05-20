from __future__ import division
import cjson
from collections import defaultdict
from operator import itemgetter
gpdp='./gpd2_%s'
bb=defaultdict(dict)
bbb=defaultdict(dict)
bb_with_f=defaultdict(dict)
ll=['atlanta', 'new_york', 'la', 'seatle', 'houston', 'dallas', 'indiana', 'miami', 'sf', 'chicago']
out1=open('cnts-v3','w')
out2=open('cnts1-v3','w')
out3=open('bbf-v3','w')
lldict={}
for key in ll:
    gpd=gpdp%key
    inf=open(gpd,'r')
    gpddict=cjson.decode(inf.readline())
    for key,value in gpddict.iteritems():
        #bb[key][value]=bb[key].get(value,0)+1
        bb[key][value[0]]=bb[key].get(value[0],0)+1
        bbb[key][value[0]]=bbb[key].get(value[0],0)+value[1]
        #bb_with_f[key][value[0]]=bb_with_f[key].get(value[0],0)+value[2]*value[1]
#        print value[2]
bb_with_f=bbb
bb1=defaultdict(list)
cnt=0
root=0
for key,value in bb.iteritems():
    xxx=sorted(value.items(),key=itemgetter(1),reverse=1)
    bb_f=sorted(bbb[key].items(),key=itemgetter(1),reverse=1)
    prb=bb_f
    #bb_f=sorted(bb_with_f[key].items(),key=itemgetter(1),reverse=1)
#    print key,xxx
    print>>out1,key,xxx,prb,bb_f
    lldict[key]=prb[:2]
    l_cnt=0
    for i in range(len(xxx)):
        l_cnt+=xxx[i][1]
    if len(xxx)==1 and xxx[0][0]=='ROOT' and xxx[0][1]>=5:
        bb1[key]=xxx[0]
    elif len(xxx)==1 and xxx[0][0]!='ROOT' and xxx[0][1]>=3:
        bb1[key]=xxx[0]
    elif len(xxx)>1 and xxx[0][0]!='ROOT' and xxx[0][1]-xxx[1][1]>=2:
        bb1[key]=xxx[0]
    elif len(xxx)>1 and xxx[0][0]!='ROOT' and prb[0][1]-prb[1][1]>=1:
        bb1[key]=prb[0]
    else:
        pass
        
cnt=0     
root=0
for key,value in bb1.iteritems():
    if value[0]=='ROOT':
        root+=1
    if value[0] in key:
        cnt+=1
print len(bb1) #with phrase
print cnt #without phrase
print root
outfile=open('backbone-cen-v3','w')
outfile.write(cjson.encode(bb1))
out3.write(cjson.encode(lldict))


