import cjson
import sys
#argvs gpd_local gpd_backbone
infile=open('../backbone/local/centrality_new/backbone-conf-2','r')
infile1=open('./backbone-2','r')
test=open('./dist_inf', 'w')
local=cjson.decode(infile.readline())
general=cjson.decode(infile1.readline())

for key,value in general.iteritems():
    if key in local.keys() and local[key][0] != value[0]:
        print>>test, key,'-',value[0],'--', local[key][0]
infile1.close()

