from __future__ import division
import cjson
from collections import defaultdict
from operator import itemgetter
gpdp='../backbone1/gpd_%s'
bb=defaultdict(dict)
bbb=defaultdict(dict)
ll=['atlanta', 'new_york', 'la', 'seatle', 'houston', 'dallas', 'indiana', 'miami', 'sf', 'chicago']
out1=open('cnts','w')
out2=open('cnts1','w')
for key in ll:
    gpd=gpdp%key
    inf=open(gpd,'r')
    gpddict=cjson.decode(inf.readline())
    for key,value in gpddict.iteritems():
        #bb[key][value]=bb[key].get(value,0)+1
        bb[key][value[0]]=bb[key].get(value[0],0)+1
        bbb[key][value[0]]=bbb[key].get(value[0],0)+value[1]
bb1=defaultdict(list)
cnt=0
for key,value in bb.iteritems():
    xxx=sorted(value.items(),key=itemgetter(1),reverse=1)
    prb=sorted(bbb[key].items(),key=itemgetter(1),reverse=1)
#    print key,xxx
    print>>out1,key,xxx,prb
    if len(xxx)>=2 and xxx[0][1]==xxx[1][1] and xxx[0][1]>=2:
        #print>>out2,key,xxx,prb
        eqlist=[]
        for item in xxx:
            if xxx[0][1]==item[1]:
#                print bbb[key],item[0]
                eqlist.append([item[0],bbb[key][item[0]]])
        master=sorted(eqlist,key=itemgetter(1),reverse=1)[0]
        master=master[:-1]
        master.append(xxx[0][1])
        bb1[key]=master
    
    elif len(xxx)==1 and xxx[0][1]>=2:
        bb1[key]=xxx[0]
    elif len(xxx)>=2 and xxx[0][1]!=xxx[1][1] and xxx[0][1]>=2:
        #print xxx[0],bbb[key]
        if xxx[0][0]=='ROOT' and prb[0][1]>=1:
            print '##',key,xxx,prb
    #        bb1[key]=prb[0]
    #    elif xxx[0][0]=='ROOT' and prb[0][1]<1:
    #        pass
    #    elif xxx[0][0]=='ROOT' and len(xxx)>=2 and xxx[0][1]<=3:
    #        print key,xxx
        else:
            bb1[key]=xxx[0]
    elif len(xxx)>=2 and prb[0][1]>0.5 and prb[0][1]-prb[1][1]>0.2:
        print >>out2,key,xxx,prb
    elif len(xxx)==1 and prb[0][1]>0.5:
        print >>out2,key,xxx,prb
    else:
        pass
    if ' 'not in key:
        cnt+=1
    else:
        pass
        #print '--',key,xxx
print len(bb1) #with phrase
print cnt #without phrase
outfile=open('backbone-conf-2-0.4','w')
outfile.write(cjson.encode(bb1))



