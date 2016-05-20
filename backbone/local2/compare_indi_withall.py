import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open(sys.argv[1],'r')
infile1=open(sys.argv[2],'r')
infile2=open(sys.argv[3],'r')
test=open(sys.argv[4], 'w')
local=cjson.decode(infile.readline())
general=cjson.decode(infile1.readline())
bb=cjson.decode(infile2.readline())

for key,value in local.iteritems():
    if key not in general.keys():
        print>>test, key,'-indi--',value
#        pass
    elif key in general.keys() and key not in bb.keys() and general[key][0] != local[key][0]:
        print>> test,key,'-indi--',local[key][0],'-all--',general[key][0]
infile1.close()
infile2.close()

