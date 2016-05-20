import cjson
infile1='./graph/gpd2_ny'
infile2='./graph/gpd2_all'
outfile=open('./ny','w')
nm=open(infile1,'r')
lc=open(infile2,'r')
nm=cjson.decode(nm.readline())
lc=cjson.decode(lc.readline())
for key, value in lc.iteritems():
    if key in nm.keys():
        if nm[key][0]!=value[0]:
            print>>outfile, key,'-',value[0],'-',nm[key][0]
#    else:print >> outfile, '---',key,'-',value
