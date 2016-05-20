import cjson
infile1='./gpd_la'
infile2='../backbone/local/centrality_new/gpd_la'
outfile=open('./nm_ll','w')
nm=open(infile1,'r')
lc=open(infile2,'r')
nm=cjson.decode(nm.readline())
lc=cjson.decode(lc.readline())
for key, value in nm.iteritems():
    if key in lc.keys():
        if lc[key][0]!=value[0]:
            print>>outfile, key,'-',value[0],'-',lc[key][0]
