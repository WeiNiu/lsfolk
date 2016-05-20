import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open('../backbone-conf-2','r')
infile1=open('./backbone-conf-2','r')
test=open('./difference-bbs', 'w')
bb1=cjson.decode(infile.readline())
bb=cjson.decode(infile1.readline())

for key,value in bb1.iteritems():
    if key in bb.keys() and bb[key][0] != value[0]:
        print>>test, key,'-',value[0],'--', bb[key][0]
infile1.close()

