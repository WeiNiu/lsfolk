import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open(sys.argv[1],'r')
infile1=open(sys.argv[2],'r')
test=open(sys.argv[3], 'w')
test1=open(sys.argv[4],'w')
local=cjson.decode(infile.readline())
general=cjson.decode(infile1.readline())

#for key,value in local.iteritems():
#    if key not in general.keys():
#        print>>test, key,'-',value
#infile1.close()

for key,value in local.iteritems():
#    print general[key],local[key]
    if key in general.keys() and general[key][0]!=local[key][0]:
        print >>test,key,'-',general[key],local[key]
    elif key not in general.keys():
        print >>test1,key,value
