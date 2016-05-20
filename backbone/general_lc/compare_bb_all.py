import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open('../general2/gpd3_5','r')
infile1=open('gpd3_lc8lc','r')
test=open('./difference', 'w')
local=cjson.decode(infile1.readline())
general=cjson.decode(infile.readline())

for key,value in general.iteritems():
    if key in local.keys() and local[key][0] != value[0]:
        print>>test, key,'-ge--',value[0],'-lc--', local[key][0]
    elif key not in local.keys():
        print>>test,'---',key,'ge',value[0]
infile1.close()

