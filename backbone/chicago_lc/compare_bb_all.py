import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open('../backbone1/gpd1_all','r')
infile1=open('backbone-conf-5-v1-p','r')
test=open('./difference5-v1-p', 'w')
local=cjson.decode(infile.readline())
general=cjson.decode(infile1.readline())

for key,value in general.iteritems():
    if key in local.keys() and local[key][0] != value[0]:
        print>>test, key,'-bb--',value[0],'-all--', local[key][0]
    elif key not in local.keys():
        print>>test,'---',key,'bb',value[0]
infile1.close()

