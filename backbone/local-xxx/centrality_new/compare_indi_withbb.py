import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open(sys.argv[1],'r')
infile1=open(sys.argv[2],'r')
test=open(sys.argv[3], 'w')
local=cjson.decode(infile.readline())
general=cjson.decode(infile1.readline())

for key,value in local.iteritems():
    if key not in general.keys():
        print>>test, key,'-',value
infile1.close()

