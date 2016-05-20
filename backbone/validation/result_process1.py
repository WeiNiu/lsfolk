from __future__ import division
import cjson
location=['ny','sf','miami','la','hou','seattle','dallas','chi']
outfile=open('result2','w')

for loc in location:
    a=0
    blist=[]
    clist=[]
    infile=open('./acc_mix_%s'%loc+'2','r')
    #print infile
    l=eval(infile.readline())
    t=l[0]
    print l
    for i in range(5):
        a=t[i][0]
        blist.append(round(t[i][1],4))
        clist.append(round(t[i][2],4))
    blist.append(sum(blist)/5)
    clist.append(sum(clist)/5)
    outfile.write(loc+'\n')
    outfile.write(cjson.encode(blist)+'\n')
    outfile.write(cjson.encode(clist)+'\n')
    outfile.write(str(l[1])+'\n')
    outfile.write(str(a)+'\n')
    outfile.write('\n')

