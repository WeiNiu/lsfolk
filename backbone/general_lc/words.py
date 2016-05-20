from pattern.en import parse
import cjson
infile='gpd_la'
outfile=open('wordinfo','w')
infile=open(infile,'r')
dictt=cjson.decode(infile.readline())
for key,value in dictt.iteritems():
    print >>outfile,key,parse(key).split()[0]
