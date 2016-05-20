import cjson
from operator import itemgetter
from collections import defaultdict
from copy import deepcopy
infile='/spare/wei/local/rulelist_en_ch3-log'

outfile='/spare/wei/local/root_dict_ch3-log'
#infile='rulelist_lt10_schz_0.6'
#outfile='root_dict_lt10_schz_0.6'
outfile=open(outfile,'w')
root_dict=defaultdict(list)
for line in open(infile,'r'):
    line=cjson.decode(line)
    #print line[0]
    root_dict[line[0]].append([line[1],line[2]])
    #root_dict[line[1]].append([line[0],line[2],line[3],line[2]*line[3]])
sorted_root_dict=defaultdict(list)
for key,value in root_dict.iteritems():
    v=deepcopy(value)
    v=sorted(v,key=itemgetter(1),reverse=1)
    sorted_root_dict[key]=v
for key,value in sorted_root_dict.iteritems():
    outfile.write(cjson.encode([key,value])+'\n')
