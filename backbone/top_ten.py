import cjson
import sys
from operator import itemgetter
infile=open(sys.argv[1],'r')
outfile=open(sys.argv[2],'a')

dictt=cjson.decode(infile.readline())
top=sorted(dictt.items(),key=itemgetter(1),reverse=1)[:19]
key,value=[],[]

for item in top:
    key.append(item[0])
    value.append(item[1])
outfile.write(cjson.encode([key,value])+'\n')

