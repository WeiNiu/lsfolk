import cjson
import sys
#argvs gpd_local gpd_backbone
infile1=open('./gpd3_houston','r')
infile=open('./gpd1_houston','r')
test=open('./diff-v1-p', 'w')
local=cjson.decode(infile.readline())
general=cjson.decode(infile1.readline())

for key,value in general.iteritems():
    if key in local.keys() and local[key][0] != value[0]:
        print>>test, key,'-complete--',value[0],'-partial--', local[key][0]
    elif key not in local.keys():
        print>>test,'---',key,'-complete-',value[0]
infile1.close()

