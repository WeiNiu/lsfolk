from __future__ import division
import cjson
from collections import defaultdict
from operator import itemgetter
gpdp='./gpd_1%s'
bb=defaultdict(dict)
bbb=defaultdict(dict)
bb_with_f=defaultdict(dict)
ll=['atlanta', 'new_york', 'la', 'seatle', 'houston', 'dallas', 'indiana', 'miami', 'sf', 'chicago']
out1=open('cnts-v1-p','w')
out2=open('cnts1-v1-p','w')
out3=open('bbf-v1-p','w')
lldict={}
for key in ll:
    gpd=gpdp%key
    inf=open(gpd,'r')
    gpddict=cjson.decode(inf.readline())
    for key,value in gpddict.iteritems():
        #bb[key][value]=bb[key].get(value,0)+1
        bb[key][value[0]]=bb[key].get(value[0],0)+1
        bbb[key][value[0]]=bbb[key].get(value[0],0)+value[1]
        bb_with_f[key][value[0]]=bb_with_f[key].get(value[0],0)+value[2]*value[1]
#        print value[2]
bb1=defaultdict(list)
cnt=0
root=0
for key,value in bb.iteritems():
    xxx=sorted(value.items(),key=itemgetter(1),reverse=1)
    prb=sorted(bbb[key].items(),key=itemgetter(1),reverse=1)
    bb_f=sorted(bb_with_f[key].items(),key=itemgetter(1),reverse=1)
#    print key,xxx
    print>>out1,key,xxx,prb,bb_f
    lldict[key]=prb[:2]
    l_cnt=0
    for i in range(len(xxx)):
        l_cnt+=xxx[i][1]

    if  len(xxx)==1 and l_cnt>=3:
        if xxx[0][1]>=2 and xxx[0][0]!='ROOT':
            bb1[key]=xxx[0]
        elif xxx[0][1]>=5 and xxx[0][0]=='ROOT':
            bb1[key]=xxx[0]
            root+=1
        else:continue
    
    elif len(xxx)>=2 and l_cnt>3:
        #if key=='cs':
        #    print key
        if xxx[0][1]>=2 and xxx[0][1]==xxx[1][1] and xxx[0][1]>=0.3*l_cnt:
            if xxx[0][0]=='ROOT':
                bb1[key]=xxx[1]
            elif xxx[1][0]=='ROOT':
                bb1[key]=xxx[0]
            else:
                top=[prb[0][0],prb[1][0]]
                
                if bb_with_f[key][top[0]]>=bb_with_f[key][top[1]]:
                    bb1[key]=[top[0],bb_with_f[key][top[0]]]
                else:
                    bb1[key]=[top[1],bb_with_f[key][top[1]]]
                #if key=='telecom':
                #    print bb1[key],bb_with_f[key][top[0]],bb_with_f[key][top[1]]
        elif xxx[0][1]>=2 and xxx[0][1]!=xxx[1][1]:
            #if key=='cs':
            #    print l_cnt, xxx[0][1]
            if xxx[0][0]=='ROOT'  and xxx[1][1]>=2 and xxx[1][1]>=0.4*xxx[0][1]: 
                bb1[key]=bb_f[0]
            elif xxx[0][0]=='ROOT' and l_cnt>2*xxx[0][1]:
                if value[bb_f[0][0]]>0.3*l_cnt:
                    bb1[key]=bb_f[0]
                else:
                    pass
            elif xxx[0][0]=='ROOT' and xxx[0][1]>7:
                bb1[key]=xxx[0]
            elif xxx[0][0]=='ROOT' and l_cnt<1.5*xxx[0][1]:
                pass
            else:
                #if key=='cs':
                #    print key
                if xxx[0][1]>=0.3*l_cnt:
                    bb1[key]=xxx[0]
                else:
                    #print key
                    pass
        else:
            print key
            pass
        #print key,bb1[key]
        #if bb1[key][0]=='ROOT':
        #    root+=1
        #    print key
    else:
        pass
    if ' 'not in key:
        cnt+=1
        #print '--',key,xxx
root=0
for key,value in bb1.iteritems():
    if value[0]=='ROOT':
        root+=1
print len(bb1) #with phrase
print cnt #without phrase
print root
outfile=open('backbone-conf-5-v1-p','w')
outfile.write(cjson.encode(bb1))
out3.write(cjson.encode(lldict))


