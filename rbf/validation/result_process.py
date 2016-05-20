from __future__ import division
import cjson
location=['ny','sf','miami','la','hou','seattle','dallas','chi']
outfile=open('result-rbf-1','w')

onelist=[]
fivelist=[]
onecnt=[]
fivecnt=[]
can=[]
for loc in location:
    a=0
    blist=[]
    clist=[]
    infile=open('./acc_rbf_%s'%loc+'2','r')
    #print infile
    l=eval(infile.readline())
    t=l[0]
    can.append(l[1])
    print l
    for i in range(5):
        a=t[i][0]
        blist.append(round(t[i][1],4))
        clist.append(round(t[i][2],4))
    onelist.append(blist[0])
    onecnt.append(clist[0])
    fivelist.append(sum(blist)/5)
    fivecnt.append(sum(clist)/5)
onelist.append(sum(onelist)/len(onelist))
fivelist.append(sum(fivelist)/len(fivelist))
onecnt.append(sum(onecnt)/len(onecnt))
fivecnt.append(sum(fivecnt)/len(fivecnt))
can.append(sum(can)/len(can))
    #outfile.write(loc+'\n')
    #outfile.write(cjson.encode(blist)+'\n')
    #outfile.write(cjson.encode(clist)+'\n')
    #outfile.write(str(l[1])+'\n')
    #outfile.write(str(a)+'\n')
    #outfile.write('\n')
outfile.write(cjson.encode(onelist)+'\n')
outfile.write(cjson.encode(fivelist)+'\n')
outfile.write(cjson.encode(onecnt)+'\n')
outfile.write(cjson.encode(fivecnt)+'\n')
outfile.write(cjson.encode(can)+'\n')
