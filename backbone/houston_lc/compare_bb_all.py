import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open('./gpd3_lchou','r')
infile1=open('../lc/gpd_hou','r')
test=open('./difference5-v1-p', 'w')
local=cjson.decode(infile.readline())
general=cjson.decode(infile1.readline())

for key,value in general.iteritems():
    if key in local.keys() and local[key][0] != value[0]:
        print>>test, key,'-bb--',value[0],'-all--', local[key][0]
    elif key not in local.keys():
        print>>test,'---',key,'bb',value[0]
infile1.close()

