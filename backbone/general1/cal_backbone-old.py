import cjson
from collections import defaultdict
from operator import itemgetter
gpdp='../backbone1/gpd_%s'
bb=defaultdict(dict)
ll=['atlanta', 'new_york', 'la', 'seatle', 'houston', 'dallas', 'indiana', 'miami', 'sf', 'chicago']
out1=open('cnts','w')
for key in ll:
    gpd=gpdp%key
    inf=open(gpd,'r')
    gpddict=cjson.decode(inf.readline())
    for key,value in gpddict.iteritems():
        bb[key][value]=bb[key].get(value,0)+1
bb1=defaultdict(list)
cnt=0
for key,value in bb.iteritems():
    xxx=sorted(value.items(),key=itemgetter(1),reverse=1)
    print xxx
    if len(xxx)>=2 and xxx[0][1]==xxx[1][1] and xxx[0][1]>=2:
        print>>out1,key,xxx[0],xxx[1]
        if xxx[0][0]=='ROOT':
            xxx=xxx[1]
    xxx=xxx[0]
    if xxx[1]>=2:
        bb1[key]=xxx[0]
        if ' 'not in key:
            cnt+=1
        else:
            print key,xxx
print len(bb1)
print cnt
outfile=open('backbone-2','w')
outfile.write(cjson.encode(bb1))



