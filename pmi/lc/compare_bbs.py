import cjson
infile1='./local/gpd_sf'#new_york'#'./local/backbone-conf-5-v1-p'
#infile2='./local4/gpd_2houston'#new_york'#
infile2='./gpd1_sf'#0.3new_york'#'./backbone-conf-5-v1-p'
outfile=open('./bbs-lc-nm-sf','w')
nm=open(infile1,'r')
lc=open(infile2,'r')
nm=cjson.decode(nm.readline())
lc=cjson.decode(lc.readline())
for key, value in lc.iteritems():
    if key in nm.keys():
        if nm[key][0]!=value[0]:
            print>>outfile, key,'-',value[0],'-',nm[key][0]
    else:print >> outfile, '-0--',key,'-',value[0]
for key,value in nm.iteritems():
    if key not in lc.keys():
        print>>outfile,key,'-',value[0],'-1--'
