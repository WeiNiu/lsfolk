import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open('gpd_houston','r')
infile1=open('gpd_dallas','r')

test=open('diff_da_h', 'w')
l1=cjson.decode(infile.readline())
l2=cjson.decode(infile1.readline())
#bb=cjson.decode(infile2.readline())

for key,value in l1.iteritems():
    if key not in l2.keys():
        print>>test,'--', key,'---',value[0]
#        pass
    elif key in l2.keys() and l2[key][0] != l1[key][0]:
        print>> test,key,'---',l1[key][0],'---',l2[key][0]
for key,value in l2.iteritems():
    if key not in l1.keys():
        print>>test,key,'---',value[0],'--'
infile1.close()
#infile2.close()

