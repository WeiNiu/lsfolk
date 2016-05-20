import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open('./gpd_hou','r')
infile1=open('../general1/gpd3_all','r')
test=open('./difference2', 'w')
local=cjson.decode(infile.readline())
general=cjson.decode(infile1.readline())

for key,value in general.iteritems():
    if key in local.keys() and local[key][0] != value[0]:
        print>>test, key,'--all--',value[0],'--c--', local[key][0]
#    elif key not in local.keys():
#        print>>test,'--all--',key,'p',value[0]
infile1.close()

