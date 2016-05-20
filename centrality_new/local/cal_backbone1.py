import cjson
from collections import defaultdict
from operator import itemgetter
gpdp='gpd_%s'
bb=defaultdict(dict)
bbb=defaultdict(dict)
ll=['atlanta', 'new_york', 'la', 'seatle', 'houston', 'dallas', 'indiana', 'miami', 'sf', 'chicago']
out1=open('cnts','w')
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
    print key,xxx
    if len(xxx)>=2 and xxx[0][1]==xxx[1][1] and xxx[0][1]>=3:
        print>>out1,key,xxx,prb
        eqlist=[]
        for item in xxx:
            if xxx[0][1]==item[1]:
                print bbb[key],item[0]
                eqlist.append([item[0],bbb[key][item[0]]])
        master=sorted(eqlist,key=itemgetter(1),reverse=1)[0]
        master.append(xxx[0][1])
        bb1[key]=master
    
    elif len(xxx)==1 and xxx[0][1]>=3:
        bb1[key]=xxx[0]
    elif len(xxx)>=2 and xxx[0][1]!=xxx[1][1] and xxx[0][1]>=3:
        bb1[key]=xxx[0]
    else:
        pass
    if ' 'not in key:
        cnt+=1
    else:
        print '--',key,xxx
print len(bb1) #with phrase
print cnt #without phrase
outfile=open('backbone-4','w')
outfile.write(cjson.encode(bb1))



